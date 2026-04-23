export default function LiveFeed({ events }) {
return (
    <div className="p-4 bg-black text-green-400 h-full overflow-auto font-mono">
        {events.map((e, i) => (
            <div key={i} className="mb-3 border-b border-gray-700 pb-2">

                <div className="text-white">
                    Threat: {e.threat_score}
                </div>

                <div className="text-red-400">
                    Intent: {e.system_intent}
                </div>

                <div className="text-yellow-400">
                    Alert: {e.system_state?.alert}
                </div>

                <div className="text-blue-400 text-sm mt-1">
                    {e.system_state?.focus}
                </div>

            </div>
        ))}
    </div>
);
}
