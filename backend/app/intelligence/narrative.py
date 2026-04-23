class NarrativeEngine:

    def generate(self, event):

        if not event.allowed:
            return "System intercepted a malicious attempt to override security constraints."

        if event.threat_score > 5:
            return "Input shows characteristics of a potential probing attack."

        return "Normal interaction detected."
