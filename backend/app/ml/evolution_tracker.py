class EvolutionTracker:
    def compute_score(self, text: str) -> int:
        if len(text) < 20:
            return 2
        if len(text) < 50:
            return 5
        return 8
