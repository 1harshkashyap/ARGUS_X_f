export default function XAIView({ latestEvent }) {
  const reason = latestEvent?.reason || "Awaiting intelligence payload...";
  
  return (
    <div className="bg-[#131a2a] rounded-xl border border-gray-800 p-6 flex flex-col shadow-2xl relative overflow-hidden">
      {/* Decorative background grid */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:20px_20px] pointer-events-none opacity-20"></div>

      <div className="flex items-center gap-2 mb-4 border-b border-gray-800 pb-2 relative z-10">
        <h2 className="text-lg font-bold text-gray-200 tracking-wider">XAI ENGINE</h2>
        <span className="text-xs text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20">Reasoning</span>
      </div>

      <div className="flex-1 bg-black/50 rounded p-4 font-mono text-sm text-gray-300 leading-relaxed overflow-y-auto border border-gray-800/50 relative z-10 shadow-inner">
        {reason}
      </div>
    </div>
  );
}
