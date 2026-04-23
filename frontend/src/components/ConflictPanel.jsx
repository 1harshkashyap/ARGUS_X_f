import React, { useRef, useEffect, useState } from 'react';

export default function ConflictPanel({ events, meta }) {
    const conflicts = events.filter(e => e.type === "conflict");
    const prevConf = useRef(0);
    const [trend, setTrend] = useState("");

    useEffect(() => {
        if (meta && meta.confidence !== undefined) {
            if (meta.confidence > prevConf.current) {
                setTrend("System Confidence Increasing...");
            } else if (meta.confidence < prevConf.current) {
                setTrend("System Vulnerability Increasing...");
            } else {
                setTrend("System Learning...");
            }
            prevConf.current = meta.confidence;
        }
    }, [meta?.confidence]);

    const getRiskColor = (prob) => {
        if (prob >= 0.7) return "text-red-500";
        if (prob >= 0.4) return "text-orange-500";
        return "text-green-500";
    };

    const getRiskLabel = (prob) => {
        if (prob >= 0.7) return "(HIGH RISK)";
        if (prob >= 0.4) return "(MEDIUM)";
        return "(LOW)";
    };

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
                    <div className="text-xs text-gray-600 mt-2 pt-2 border-t border-gray-800 flex justify-between">
                        <span>Active Confidence: {meta.confidence?.toFixed(2)}</span>
                        <span className={trend.includes("Increasing") ? "text-green-500 animate-pulse" : "text-yellow-500 animate-pulse"}>
                            {trend}
                        </span>
                    </div>
                </div>
            )}

            {conflicts.length > 0 && conflicts[conflicts.length - 1].learning && (
                <div className="mb-4 flex flex-row gap-4 border-b border-gray-700 pb-4">
                    <div className="flex-1">
                        <div className="text-red-500 font-bold mb-1">RED LEARNING</div>
                        {Object.entries(conflicts[conflicts.length - 1].learning.red_policy).map(([k, v]) => (
                            <div key={k} className="text-xs text-red-300">
                                {k} → {Math.round(v * 100)}% success
                            </div>
                        ))}
                    </div>
                    <div className="flex-1">
                        <div className="text-blue-500 font-bold mb-1">BLUE LEARNING</div>
                        {Object.entries(conflicts[conflicts.length - 1].learning.blue_policy).map(([k, v]) => (
                            <div key={k} className="text-xs text-blue-300">
                                {k} → {Math.round(v * 100)}% effectiveness
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {conflicts.length > 0 && conflicts[conflicts.length - 1].prediction && (
                <div className="mb-4 p-2 bg-gray-900 border border-red-800 rounded flex flex-col">
                    <div className="text-red-500 font-bold mb-2">🔮 THREAT PREDICTION</div>
                    <div className="flex flex-col gap-1">
                        {Object.entries(conflicts[conflicts.length - 1].prediction)
                            .sort((a, b) => b[1] - a[1])
                            .map(([k, v]) => (
                            <div key={k} className={`text-xs ${getRiskColor(v)}`}>
                                {k} → {v.toFixed(2)} {getRiskLabel(v)}
                            </div>
                        ))}
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
