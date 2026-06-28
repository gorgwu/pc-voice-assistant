File last updated: June 27th, 2026

# Systems

## Config & UI System

The application uses a lightweight CLI-driven configuration system.

While there are default config, users can create their own config files and add them to `configs/`. The CLI UI will pick it up automatically.

This presents 2 advantages:
* This gives the user customization options without needing to edit the bot Python files directly.
* While the config files currently only have 3 options, this allows easy scalability in the future.
    * In the future, the user could perhaps overwrite the system prompt, change voice speed...

This design keeps the runtime behavior easy to extend with new bot profiles.

## RAG System

The RAG system is optional and only activated when a `pdf` path is provided in the selected config.

The entire retrieval/indexing process is done locally, which is fine for a small RAG pipeline such as this.
* LangChain: Orchestrates loading, chunking, and vector-store integration.
* HuggingFace: Creates the embeddings that represent text semantically.
* FAISS: stores those embeddings locally and finds the closest matches for retrieval.

I'm really happy with my current implementation of a FAISS vector store:
The program saves the vector embeddings locally for the most recent pdf used in the RAG system. This allows quicker start-time for users between sessions when using the same pdf, and limits usage of the local storage as it overwrites the previous FAISS embeddings if a new pdf is used. Essentially, my program has a 1-pdf 'memory'. As this program grows, it would make sense to store more than 1 pdf's embeddings, though.

## Tooling System

A modular tool execution layer enables bots to safely accesses other Python scripts. Each tool extends a base_tool.py and allows for inheritance and polymorphism as it doesn't know the exact tool type.

For the fastest performance, tools are listed for each bot, and each tool has a name and description. Instead of reading the entire Python script to understand it, the bot will just take in the name and description.
* This also mimics Anthropic's standard of 'skills'.

There's also easy scalability, as new tools can simply be added to `tools/` and `tools/tool_registry.py` dynamically discovers tool classes in `tools/` and registers them by name.

# Main Pipeline

The core flow in `main.py` is:

1. Select configuration and load settings.
2. Clean previous temporary recordings.
3. Instantiate the selected bot and optional RAG retriever.
4. Initialize Gemini API access, audio recorder, transcriber, TTS, and player.
5. Loop:
   - Record user audio via `audio/recorder.py`.
   - Transcribe the audio to text with `audio/transcriber.py` and Gemini.
   - Retrieve RAG context if enabled.
   - Build a combined prompt using the bot’s system prompt, conversation history, available tool descriptions, and any retrieved context.
   - Generate an assistant response from `ai/gemini_client.py`.
   - If the response is a tool call JSON object, execute the tool and replace the output with the result.
   - Save the interaction to memory.
   - Render the final assistant response to speech via `speech/tts.py`.
   - Play the audio response with `speech/player.py`.

Note: There are optimizations that can be made in main, such as not importing everything at the start or simply moving main into more methods. There will definitely be changes.

# Future Ideas

Potential improvements and extension points:

- Add a web or desktop UI for config selection and/or live transcript display.
- Add formal validation for config files and tool arguments.
- Add better user-facing error messages.
    - The Google Gemini API errors are not user-friendly, those should be abstracted.
- Expand bot personas and add more bot types with custom system prompts. 
    - A Music Bot that calls the Spotify API through my tooling system, like how literally any other voice assistant can play music.
- Refactor the entire repository.

Longer ventures that I will probably put off:

- Support multi-file retrieval for RAG.
- Add a memory summarization layer to keep long conversations manageable.
- Add a system to save past conversations and allow users to revisit them.
- MCPs somehow?? Not sure if it's feasible or even needed for my project.

## End goal?

The final goal would likely be to pivot towards a multi-agent system with one 'orchestrator' agent that can call all these subagents, making the final result truly only voice-controlled, unlike needing config files.