from app.agents.conflict.engine import ConflictEngine

class SimulationEngine:
    def run(self, cycles=100):
        # CREATE FRESH ENGINE (sandbox)
        engine = ConflictEngine()

        results = []

        for _ in range(cycles):
            result = engine.run_cycle()
            results.append(result)

        return results
