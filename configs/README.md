# Config System

Each JSON file in this folder defines how the AI agent behaves.

---

## Required Fields

### bot
Defines which agent runs.

Options:
- `interview` → technical interview mode
- `textbook` → RAG-based learning assistant
- As the user, feel free to add more options!

---

### pdf
Path to a PDF used for retrieval (RAG).

Options:
- `"path/to/file.pdf"` → enables RAG
- `""` → disables RAG

---

### voice_accent
TTS accent used for speech output (required).

Options:
- `com` (US English)
- `co.uk` (UK English)
- `com.au` (Australian English)
- `co.in` (Indian English)