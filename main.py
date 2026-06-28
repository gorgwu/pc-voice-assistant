import json

from ai.gemini_client import GeminiClient

from audio.recorder import AudioRecorder
from audio.transcriber import AudioTranscriber

from speech.tts import TextToSpeech
from speech.player import AudioPlayer

from bots.interview_bot import InterviewBot
from bots.textbook_bot import TextbookBot
from bots.textfile_bot import TextFileBot

from rag.vector_store import VectorStore
from rag.retriever import Retriever
from rag.index_manager import IndexManager

from tools.tool_registry import ToolRegistry

from utils.config_loader import ConfigLoader
from utils.file_cleanup import clean_recordings
from utils.config_selector import select_config


def create_bot(
    bot_name: str
):

    if bot_name == "interview":
        return InterviewBot()

    elif bot_name == "textbook":
        return TextbookBot()

    elif bot_name == "textfile":
        return TextFileBot()

    else:

        raise Exception(
            f"Unknown bot: "
            f"{bot_name}"
        )


def main():

    # Config

    config_path = (
        select_config()
    )

    config = (
        ConfigLoader().load(
            config_path
        )
    )

    clean_recordings()

    # Bot

    bot = create_bot(
        config["bot"]
    )

    # Tool Registry

    registry = (
        ToolRegistry()
    )

    tool_descriptions = (
        registry.get_tool_descriptions(
            bot.tools
        )
    )

    # Optional RAG

    retriever = None

    pdf_path = config.get(
        "pdf",
        ""
    )

    if pdf_path:

        index_manager = (
            IndexManager()
        )

        if index_manager.needs_rebuild(
            pdf_path
        ):

            index_manager.build_index(
                pdf_path
            )

        else:

            print(
                "\nUsing existing FAISS index..."
            )

        vector_store = (
            VectorStore().load_index()
        )

        retriever = (
            Retriever(
                vector_store
            )
        )

    # AI + Audio

    gemini = GeminiClient()

    recorder = AudioRecorder()

    transcriber = (
        AudioTranscriber()
    )

    tts = TextToSpeech(
        accent=config.get(
            "voice_accent",
            "com"
        )
    )

    player = AudioPlayer()

    print(
        f"\n{bot.name} started"
    )

    # Main Loop

    while True:

        audio_path = (
            recorder.record()
        )

        user_message = (
            transcriber.transcribe(
                audio_path
            )
        )

        print(
            f"\nYou: "
            f"{user_message}"
        )

        context = ""

        if retriever:

            context = (
                retriever.retrieve(
                    user_message
                )
            )
            
        prompt = bot.build_prompt(
            user_message=user_message,
            context=context,
            tool_descriptions=tool_descriptions
        )

        response = (
            gemini.generate_response(
                prompt
            )
        )

        # Tool Execution

        if response.strip().startswith("{"):

            try:

                tool_call = (
                    json.loads(
                        response
                    )
                )

                tool_name = (
                    tool_call[
                        "tool"
                    ]
                )

                arguments = (
                    tool_call[
                        "arguments"
                    ]
                )

                if tool_name not in bot.tools:

                    raise Exception(
                        f"Tool not allowed: "
                        f"{tool_name}"
                    )

                tool_result = (
                    registry.run_tool(
                        tool_name,
                        arguments
                    )
                )

                response = (
                    str(
                        tool_result
                    )
                )

            except Exception as e:

                print(
                    f"\nTool Error: "
                    f"{e}"
                )

        print(
            f"\n{bot.name}: "
            f"{response}"
        )

        bot.save_interaction(
            user_message,
            response
        )

        audio_file = (
            tts.generate(
                response
            )
        )

        player.play(
            audio_file
        )


if __name__ == "__main__":
    main()