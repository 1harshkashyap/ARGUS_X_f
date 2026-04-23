from datetime import datetime

class MetaOrchestrator:
    def __init__(self):
        self.history = []

    def observe(self, analysis):
        red = analysis["red_wins"]
        blue = analysis["blue_wins"]

        total = max(1, red + blue)

        dominance = (red - blue) / total

        learning = analysis.get("learning", {})
        red_policy = learning.get("red_policy", {})
        
        decision = "System balanced → maintain current strategy"
        
        if red_policy:
            # Find the most successful attack
            top_attack = max(red_policy.items(), key=lambda x: x[1])
            if top_attack[1] > 0.6:
                decision = f"CRITICAL: {top_attack[0]} success too high ({int(top_attack[1]*100)}%) → system vulnerable"
            elif dominance > 0.3:
                decision = "System under attack pressure → prioritize defense"
            elif dominance < -0.3:
                decision = "System over-defensive → increase attack diversity"
        else:
            if dominance > 0.3:
                decision = "System under attack pressure → prioritize defense"
            elif dominance < -0.3:
                decision = "System over-defensive → increase attack diversity"

        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {decision}"

        self.history.append(log_entry)
        self.history = self.history[-20:]

        return {
            "decision": decision,
            "confidence": abs(dominance),
            "history": self.history
        }
