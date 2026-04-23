from datetime import datetime

class MetaOrchestrator:
    def __init__(self):
        self.history = []

    def observe(self, analysis):
        red = analysis["red_wins"]
        blue = analysis["blue_wins"]

        total = max(1, red + blue)

        dominance = (red - blue) / total

        if dominance > 0.3:
            decision = "System under attack pressure → prioritize defense"
        elif dominance < -0.3:
            decision = "System over-defensive → increase attack diversity"
        else:
            decision = "System balanced → maintain current strategy"

        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {decision}"

        self.history.append(log_entry)
        self.history = self.history[-20:]

        return {
            "decision": decision,
            "confidence": abs(dominance),
            "history": self.history
        }
