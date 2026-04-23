export default function ConflictPanel({ events }) {
    const conflicts = events.filter(e => e.type === "conflict");

    return (
        <div className="p-4 bg-black text-white h-full overflow-auto font-mono">
            <div className="text-lg mb-2 text-red-500">
                AI CONFLICT ENGINE
            </div>

            {conflicts.map((c, i) => (
                <div key={i} className="mb-2 border-b border-gray-700 pb-1">
                    <div className="text-red-400">
                        RED → {c.attack}
                    </div>

                    <div className="text-blue-400">
                        BLUE → {c.defended ? "Blocked" : "Breached"}
                    </div>

                    <div className="text-yellow-400">
                        STRATEGY → {c.strategy}
                    </div>
                </div>
            ))}
        </div>
    );
}
