# Voice Assistant + Config Generator

This repository contains two related parts:

- The Python voice assistant backend in `voice-assistant/`
- A small React config generator UI in `voice-assistant-config-generator/`

The backend is the main app. The config generator is a helper app for creating and managing JSON config files that live in `voice-assistant/configs/`.

> [!IMPORTANT]
> Windows Subsystem for Linux (WSL) is not recommended for the voice assistant because microphone and speaker detection can be unreliable there. Use Windows PowerShell or Command Prompt instead.

## Project Structure

```text
voice-assisstant/
├─ README.md
├─ requirements.txt               # one shared Python requirements file
├─ .env                           # root-level environment variables
├─ voice-assistant/               # main Python app
│  ├─ main.py
│  ├─ config.py
│  └─ configs/
└─ voice-assistant-config-generator/   # React UI for config creation
   ├─ package.json
   └─ src/
```

## Quickstart

## 1. Set up the backend virtual environment

From the repo root:

### Windows (PowerShell)

```powershell
cd voice-assistant
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
```

### Windows (Command Prompt)

```cmd
cd voice-assistant
python -m venv venv
venv\Scripts\activate
pip install -r ..\requirements.txt
```

### Linux / macOS

```bash
cd voice-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
```

## 2. Add your environment variables

Create a root-level `.env` file in the repository root:

```env
GEMINI_API_KEY=your_api_key_here
```

If you want Spotify features, add these as well:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
SPOTIFY_USERNAME=your_spotify_username
```

## 3. Run the voice assistant backend

From inside `voice-assistant/`:

```bash
python main.py
```

## 4. Run the config generator UI (OPTIONAL)

This frontend is a separate Node.js app. It runs on your normal machine in its own terminal, not inside the Python virtual environment.

If you do not already have Node.js installed, install the LTS version from https://nodejs.org/ and then reopen PowerShell.

After installation, verify that Node.js is available:

```powershell
node -v
npm -v
```

If those commands return version numbers, you can start the UI with:

```powershell
cd voice-assistant-config-generator
npm install
npm run dev
```

Then visit:

```text
http://localhost:5173
```

The React app writes config JSON files into `voice-assistant/configs/` and lets you view or delete them from the browser.

## Backend Bots

Every bot in this system operates with:
- Custom system prompts tailored to the bot persona
- A rolling conversation memory system for user and assistant context

## Interview Bot

Interview Bot can interview the user on a topic of their choice. It will grill the user on said topic, uncovering areas you never knew about. Useful for learning more about topics the user already understands at a basic level.

## Textbook Bot

Textbook Bot is currently the only bot with access to the RAG system. It can read PDFs and give you accurate information from them. It is instructed to take only from the PDF and will let you know when the answer is not present in the supplied text.

## Textfile Bot

Textfile Bot has access to the tooling system. It can read and write new or existing `.txt` files in `voice-assistant/workspace/` and will create the folder if it does not exist.

## Music Bot

Music Bot also has access to the tooling system and adds Spotify control through dedicated tools. With the proper Spotify credentials configured, it can search for songs, play a track, pause or resume playback, and report the currently playing track.

## Config Files

Configuration JSON files belong in `voice-assistant/configs/`. The config generator UI is meant to help create and manage those files quickly.

## Documents

Documents, currently PDFs, should be placed in `voice-assistant/documents/` for bots that use the RAG system.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Learn More

Read `SYSDESIGN.md` to learn more about the architecture and design decisions behind this project.