import sys
import os
import importlib
import json

# Change to script directory so relative paths work
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

from ai.gemini_client import GeminiClient

from audio.recorder import AudioRecorder
from audio.transcriber import AudioTranscriber

from speech.tts import TextToSpeech
from speech.player import AudioPlayer

from utils.config_loader import ConfigLoader
from utils.file_cleanup import clean_recordings
from utils.config_selector import select_config


BOT_REGISTRY = {
    "interview": (
        "bots.interview_bot",
        "InterviewBot"
    ),
    "textbook": (
        "bots.textbook_bot",
        "TextbookBot"
    ),
    "textfile": (
        "bots.textfile_bot",
        "TextFileBot"
    ),
    "music": (
        "bots.music_bot",
        "MusicBot"
    )
}


def create_bot(
    bot_name: str
):

    if bot_name not in BOT_REGISTRY:

        raise Exception(
            f"Unknown bot: "
            f"{bot_name}"
        )

    module_name, class_name = (
        BOT_REGISTRY[bot_name]
    )

    module = importlib.import_module(
        module_name
    )

    bot_class = getattr(
        module,
        class_name
    )

    return bot_class()


def setup_tools(bot):

    from tools.tool_registry import (
        ToolRegistry
    )

    registry = ToolRegistry()

    tool_descriptions = (
        registry.get_tool_descriptions(
            bot.tools
        )
    )

    return registry, tool_descriptions


def setup_rag(config, bot):

    pdf_path = config.get(
        "pdf",
        ""
    )

    if not pdf_path:
        return None

    from rag.index_manager import (
        IndexManager
    )
    from rag.vector_store import (
        VectorStore
    )
    from rag.retriever import (
        Retriever
    )

    index_manager = IndexManager()

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

    vector_store = VectorStore().load_index()

    return Retriever(vector_store)


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

    # Optional Tooling

    registry = None
    tool_descriptions = ""

    if bot.has_capability("tools"):

        registry, tool_descriptions = (
            setup_tools(bot)
        )

    # Optional RAG

    retriever = None

    if bot.has_capability("rag"):

        retriever = (
            setup_rag(
                config,
                bot
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