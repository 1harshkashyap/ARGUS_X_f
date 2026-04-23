class GlobalState:
    def __init__(self):
        self.alert_level = "LOW"
        self.focus = "None"
        self.confidence = 0.0

    def update(self, event):
        score = event.threat_score

        if score > 7:
            self.alert_level = "HIGH"
        elif score > 4:
            self.alert_level = "MEDIUM"
        else:
            self.alert_level = "LOW"

        self.focus = event.data.get("intent", "Unknown")
        self.confidence = min(1.0, score / 10)

        return self
