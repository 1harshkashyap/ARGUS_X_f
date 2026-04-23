import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.simulation.engine import SimulationEngine
from app.simulation.analyzer import SimulationAnalyzer

if __name__ == "__main__":
    sim_engine = SimulationEngine()
    sim_analyzer = SimulationAnalyzer()
    
    results = sim_engine.run(100)
    analysis = sim_analyzer.analyze(results)
    
    output = {
        "analysis": analysis,
        "sample": results[:3]
    }
    
    print(json.dumps(output, indent=2))
