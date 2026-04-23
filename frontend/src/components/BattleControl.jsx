export default function BattleControl() {

const runBattle = async () => {
    await fetch("/api/v1/battle");
};

return (
    <button
        onClick={runBattle}
        className="bg-red-600 text-white px-4 py-2 rounded"
    >
        Run AI Battle
    </button>
);

}
