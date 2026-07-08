# Quickstart

> [!IMPORTANT]
> Windows Subsystem for Linux (WSL) is not recommended while using this application. Audio input/output devices are often not detected correctly, which may prevent microphone and speaker functionality from working as expected. On Windows, use PowerShell or Command Prompt instead.

## 1. Create a Virtual Environment

### Windows

```powershell
cd voice-assistant
python -m venv venv
```

### Linux / macOS

```bash
cd voice-assistant
python3 -m venv venv
```

## 2. Activate the Virtual Environment

### Windows (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)

```cmd
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Add Your Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Note: Models can be configured in `voice-assistant/config.py`

## 5. Optional: Add Spotify Credentials

If you want to use the music bot, add these environment variables as well:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
SPOTIFY_USERNAME=your_spotify_username
```

You will also need a Spotify Developer app to fill in those credentials.

## 6. Run the Application

Run directly from the voice-assistant subdirectory:

```bash
python main.py
```

# Current Agents/Bots

Every bot in this system operates with:
* **Custom System Prompts**: Tailored personas, constraints, and instructions for specific roles.
* **Standard Memory System**: A rolling conversation history where past user and assistant messages feed directly back into the context window.

Note: System prompts will slowly be refined as bots will be continously tested. The bots are fair from perfect. The upside of AI is that it's non-deterministic. The downside of AI is that it's non-deterministic (it becomes difficult to quantify the AI's success and the quality of the system prompts).

## Interview Bot

Interview Bot can interview the user on a topic of their choice. It will grill the user on said topic, uncovering areas you never knew about. Useful to learn more about topics that the user already have a basic understanding of.

## Textbook Bot

Textbook Bot is currently the only bot with access to the RAG system. It can read PDFs and give you accurate information from them. It is instructed to solely take from the PDF, and will let you know if your question cannot be answered from the text in the PDF. Great for note-taking purposes, where the user can transcribe to study.

## Textfile Bot

Textfile Bot has access to the tooling system. It can read/write new or existing .txt files in `voice-assistant/workspace/`, and will create the folder if it does not exist. Helpful to create reminders or quick text files. As the system is built on Gemini, it can also translate and save the user's input into text in another language.

## Music Bot

Music Bot has also has access to the tooling system, and adds Spotify control through these tools. With Spotify credentials configured, it can search for songs, play a track, pause or resume playback, and report the currently playing track.

# Config Files

Additional versions of each bot can be configured in `voice-assistant/configs/`. See `voice-assistant/configs/README.md` for additional instructions.

# Documents

Documents (currently only PDFs) should be put in `voice-assistant/documents/` to be read by a bot that can access the RAG system.

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Want to Learn More?

Read `SYSDESIGN.md` to learn more about my system design process, and the thought that went into this project to ensure the best user and developer experience (scalability, reliability, performance, security, etc.)