class EvolutionEngine:
    def __init__(self):
        self.adjustment = {
            "blue_bias": 0.8,
            "red_exploration": 0.3
        }

    def evolve(self, analysis, meta=None):
        red = analysis["red_wins"]
        blue = analysis["blue_wins"]

        total = max(1, red + blue)

        # imbalance ratio (-1 to +1)
        imbalance = (red - blue) / total

        # smooth update instead of hard increments
        self.adjustment["blue_bias"] += (-imbalance) * 0.1
        self.adjustment["red_exploration"] += (abs(imbalance)) * 0.05

        # 🔥 META INFLUENCE (NEW)
        if meta:
            decision = meta.get("decision", "")

            if "over-defensive" in decision:
                self.adjustment["red_exploration"] += 0.05

            elif "attack pressure" in decision:
                self.adjustment["blue_bias"] += 0.05

        # clamp values safely
        self.adjustment["blue_bias"] = max(0.1, min(1.0, self.adjustment["blue_bias"]))
        self.adjustment["red_exploration"] = max(0.05, min(0.9, self.adjustment["red_exploration"]))

        return self.adjustment
