import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.simulation.engine import SimulationEngine
from app.simulation.analyzer import SimulationAnalyzer
from app.evolution.engine import EvolutionEngine
from app.meta.orchestrator import MetaOrchestrator

if __name__ == "__main__":
    sim_engine = SimulationEngine()
    sim_analyzer = SimulationAnalyzer()
    evo_engine = EvolutionEngine()
    meta_orchestrator = MetaOrchestrator()
    
    results = sim_engine.run(100)
    analysis = sim_analyzer.analyze(results)
    meta = meta_orchestrator.observe(analysis)
    adjustments = evo_engine.evolve(analysis, meta)
    
    output = {
        "analysis": analysis,
        "evolution": adjustments,
        "meta": meta,
        "sample": results[:1]
    }
    
    print(json.dumps(output, indent=2))
