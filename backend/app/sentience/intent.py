class SystemIntent:
    def decide(self, event):
        if not event.allowed:
            return "Contain threat"

        if event.threat_score > 5:
            return "Monitor escalation"

        return "Normal operation"
