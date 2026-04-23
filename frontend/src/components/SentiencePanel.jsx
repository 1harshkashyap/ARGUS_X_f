export default function SentiencePanel({ latest }) {
if (!latest) return null;

const state = latest.system_state || {};

return (
    <div className="p-4 bg-gray-900 text-white h-full">

        <div className="text-lg font-bold mb-2">SYSTEM STATE</div>

        <div>Alert: {state.alert}</div>
        <div>Focus: {state.focus}</div>
        <div>Confidence: {state.confidence}</div>

        <div className="mt-4 text-lg font-bold">SYSTEM INTENT</div>
        <div className="text-red-400">{latest.system_intent}</div>

    </div>
);
}
