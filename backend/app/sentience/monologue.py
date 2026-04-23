import time

class Monologue:
    def __init__(self):
        self.history = []

    def generate(self, event):
        ts = time.strftime("%H:%M:%S")

        if not event.allowed:
            msg = f"[{ts}] Threat detected. Initiating containment..."
        elif event.threat_score > 5:
            msg = f"[{ts}] Suspicious behavior observed..."
        else:
            msg = f"[{ts}] System stable. Monitoring..."

        self.history.append(msg)

        # keep last 50 messages
        self.history = self.history[-50:]

        return self.history
