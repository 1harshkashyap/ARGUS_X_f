from app.agents.conflict.engine import ConflictEngine

class SimulationEngine:
    def __init__(self):
        self.engine = ConflictEngine()

    def run(self, cycles=100):
        results = []

        for _ in range(cycles):
            result = self.engine.run_cycle()
            results.append(result)

        return results
