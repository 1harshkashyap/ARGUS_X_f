export default function MonologueView({ latest }) {
const log = latest?.monologue || [];

return (
    <div className="p-4 bg-black text-green-400 h-full overflow-auto font-mono">

        {log.map((line, i) => (
            <div key={i}>{line}</div>
        ))}

    </div>
);
}
