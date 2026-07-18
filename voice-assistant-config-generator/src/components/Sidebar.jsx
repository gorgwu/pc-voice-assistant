import { useMemo, useState } from "react";

export default function Sidebar({
    configs,
    selected,
    onSelect,
    onCreate,
}) {
    const [search, setSearch] = useState("");

    const filteredConfigs = useMemo(() => {
        const query = search.toLowerCase().trim();

        return [...configs]
            .sort((a, b) => a.name.localeCompare(b.name))
            .filter((config) => {
                return (
                    config.name.toLowerCase().includes(query) ||
                    config.file_name.toLowerCase().includes(query)
                );
            });
    }, [configs, search]);

    return (
        <aside className="sidebar">

            <div className="sidebar-header">

                <div>
                    <h2>📁 Configurations</h2>
                    <p>{configs.length} configuration{configs.length !== 1 ? "s" : ""}</p>
                </div>

                <button
                    className="new-config-btn"
                    onClick={onCreate}
                >
                    + New
                </button>

            </div>

            <input
                className="search-box"
                placeholder="Search configurations..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />

            <div className="config-list">

                {filteredConfigs.length === 0 && (
                    <div className="empty-sidebar">
                        <div className="empty-folder">📂</div>
                        <strong>No configurations</strong>
                        <span>
                            Create one to get started.
                        </span>
                    </div>
                )}

                {filteredConfigs.map((config) => (

                    <div
                        key={config.file_name}
                        className={`config-item ${
                            selected?.file_name === config.file_name
                                ? "selected"
                                : ""
                        }`}
                        onClick={() => onSelect(config)}
                    >

                        <div className="file-icon">
                            📄
                        </div>

                        <div className="file-details">

                            <div className="config-name">
                                {config.name}
                            </div>

                            <div className="config-file">
                                {config.file_name}
                            </div>

                        </div>

                    </div>

                ))}

            </div>

        </aside>
    );
}