from app.ml.evolution_tracker import EvolutionTracker

class EvolutionProcessor:
    def __init__(self):
        self.tracker = EvolutionTracker()

    def handle(self, event):
        score = self.tracker.compute_score(event.text)

        return {
            "evolution_score": score,
            "threat_score": 6 if score > 6 else 0
        }
