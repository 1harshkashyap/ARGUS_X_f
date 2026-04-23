export default function MetricsPanel({ latest }) {
if (!latest) return null;

return (
    <div className="p-4 bg-gray-900 text-white">
        <div>Block Rate: {latest.block_rate}</div>
        <div>Avg Threat: {latest.avg_threat}</div>
        <div>Mode: {latest.mode}</div>
    </div>
);

}
