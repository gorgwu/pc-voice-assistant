import { useEffect, useState } from "react";

import Sidebar from "./components/Sidebar";
import ConfigEditor from "./components/ConfigEditor";

const emptyConfig = {
    file_name: "",
    name: "",
    bot: "textfile",
    pdf: "",
    voice_accent: "com",
};

export default function App() {
    const [configs, setConfigs] = useState([]);
    const [documents, setDocuments] = useState([]);

    const [selectedConfig, setSelectedConfig] = useState(null);

    const [form, setForm] = useState(emptyConfig);

    const [message, setMessage] = useState("");

    async function loadConfigs() {
        const res = await fetch("/api/configs");
        const data = await res.json();

        setConfigs(data);
    }

    async function loadDocuments() {
        const res = await fetch("/api/documents");
        const data = await res.json();

        setDocuments(data);
    }

    useEffect(() => {
        loadConfigs();
        loadDocuments();
    }, []);

    function createNew() {
        setSelectedConfig(null);
        setForm(emptyConfig);
    }

    function openConfig(config) {
        setSelectedConfig(config);

        setForm({
            ...config,
        });
    }

    async function saveConfig() {
        const editing = selectedConfig !== null;

        const url = editing
            ? `/api/configs/${selectedConfig.file_name}`
            : "/api/configs";

        const method = editing ? "PUT" : "POST";

        const res = await fetch(url, {
            method,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(form),
        });

        const data = await res.json();

        if (!res.ok) {
            setMessage(data.error);
            return;
        }

        setMessage(
            editing
                ? "Configuration updated."
                : "Configuration created."
        );

        await loadConfigs();

        if (!editing) {
            setSelectedConfig(data);
            setForm(data);
        }
    }

    async function deleteConfig() {
        if (!selectedConfig) return;

        await fetch(
            `/api/configs/${selectedConfig.file_name}`,
            {
                method: "DELETE",
            }
        );

        setMessage("Configuration deleted.");

        createNew();

        await loadConfigs();
    }

    return (
        <div className="app-shell">

            <header className="hero">
                
                <h1> Voice Assistant
                    <br />
                    Configuration Generator
                </h1>

                <p>
                    Create and manage Voice Assistant configuration files.
                </p>
            </header>

            {message && (
                <div className="message">
                    {message}
                </div>
            )}

            <div className="dashboard">

                <Sidebar
                    configs={configs}
                    selected={selectedConfig}
                    onSelect={openConfig}
                    onCreate={createNew}
                />

                <ConfigEditor
                    form={form}
                    setForm={setForm}
                    documents={documents}
                    editing={selectedConfig !== null}
                    onSave={saveConfig}
                    onDelete={deleteConfig}
                />

            </div>

        </div>
    );
}