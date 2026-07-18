export default function ConfigEditor({
    form,
    setForm,
    documents,
    editing,
    onSave,
    onDelete,
}) {
    function update(field, value) {
        setForm({
            ...form,
            [field]: value,
        });
    }

    return (
        <main className="editor">

            <div className="editor-header">
                <h2>
                    {editing
                        ? "Edit Configuration"
                        : "New Configuration"}
                </h2>

                <p>
                    Configure your voice assistant and save it as a reusable profile.
                </p>
            </div>

            <div className="editor-card">

                <div className="form-group">
                    <label>Configuration Name</label>

                    <input
                        type="text"
                        placeholder="e.g. interview_assistant"
                        value={form.name}
                        onChange={(e) =>
                            update("name", e.target.value)
                        }
                    />
                </div>

                <div className="form-group">
                    <label>Assistant Mode</label>

                    <select
                        value={form.bot}
                        onChange={(e) =>
                            update("bot", e.target.value)
                        }
                    >
                        <option value="interview">
                            Interview
                        </option>

                        <option value="textbook">
                            Textbook
                        </option>

                        <option value="textfile">
                            Text File
                        </option>

                        <option value="music">
                            Music
                        </option>
                    </select>
                </div>

                <div className="form-group">
                    <label>PDF Document</label>

                    <select
                        value={form.pdf}
                        onChange={(e) =>
                            update("pdf", e.target.value)
                        }
                    >
                        <option value="">
                            None
                        </option>

                        {documents.map((doc) => (
                            <option
                                key={doc}
                                value={doc}
                            >
                                {doc}
                            </option>
                        ))}
                    </select>

                    <small>
                        Files are loaded automatically from
                        <code> voice-assistant/documents</code>.
                    </small>
                </div>

                <div className="form-group">
                    <label>Voice Accent</label>

                    <select
                        value={form.voice_accent}
                        onChange={(e) =>
                            update(
                                "voice_accent",
                                e.target.value
                            )
                        }
                    >
                        <option value="com">
                            🇺🇸 United States
                        </option>

                        <option value="co.uk">
                            🇬🇧 United Kingdom
                        </option>

                        <option value="com.au">
                            🇦🇺 Australia
                        </option>

                        <option value="co.in">
                            🇮🇳 India
                        </option>
                    </select>
                </div>

                <div className="button-row">

                    <button
                        className="primary-btn"
                        onClick={onSave}
                    >
                        {editing
                            ? "💾 Save Changes"
                            : "+ Create Configuration"}
                    </button>

                    {editing && (
                        <button
                            className="danger-btn"
                            onClick={onDelete}
                        >
                            🗑 Delete
                        </button>
                    )}

                </div>

            </div>

        </main>
    );
}