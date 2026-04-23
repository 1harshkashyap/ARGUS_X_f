import { useState } from "react";

export default function ReplayTimeline({ events }) {
const [index, setIndex] = useState(0);

const current = events[index];

return (
    <div className="p-4 bg-gray-900 text-white">
        <input
            type="range"
            min="0"
            max={events.length > 0 ? events.length - 1 : 0}
            value={index}
            onChange={(e) => setIndex(Number(e.target.value))}
            className="w-full"
        />

        {current && (
            <div className="mt-2">
                <div>Threat: {current.threat_score}</div>
                <div>Reason: {current.reason}</div>
                <div>Mode: {current.mode}</div>
            </div>
        )}
    </div>
);

}
