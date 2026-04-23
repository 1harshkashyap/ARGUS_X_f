export default function ConflictPanel({ events, meta }) {
    const conflicts = events.filter(e => e.type === "conflict");

    return (
        <div className="p-4 bg-black text-white h-full overflow-auto font-mono">
            <div className="text-lg mb-2 text-red-500">
                AI CONFLICT ENGINE
            </div>

            {meta && (
                <div className="mb-4 p-2 bg-gray-900 border border-purple-500 rounded flex flex-col max-h-48">
                    <div className="text-purple-400 font-bold mb-2">🧠 SYSTEM DECISION FEED</div>
                    <div className="overflow-y-auto text-xs space-y-1 font-mono">
                        {meta.history && meta.history.slice().reverse().map((m, i) => (
                            <div key={i} className={i === 0 ? "text-purple-300 font-bold" : "text-gray-500"}>
                                {m}
                            </div>
                        ))}
                    </div>
                    <div className="text-xs text-gray-600 mt-2 pt-2 border-t border-gray-800">
                        Active Confidence: {meta.confidence?.toFixed(2)}
                    </div>
                </div>
            )}

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
