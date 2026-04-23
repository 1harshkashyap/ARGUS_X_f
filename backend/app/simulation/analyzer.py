class SimulationAnalyzer:
    def analyze(self, results):
        red_wins = sum(1 for r in results if r["result"]["success"])
        blue_wins = len(results) - red_wins

        best_strategy = "Red dominant" if red_wins > blue_wins else "Blue dominant"

        return {
            "total_cycles": len(results),
            "red_wins": red_wins,
            "blue_wins": blue_wins,
            "best_strategy": best_strategy
        }
