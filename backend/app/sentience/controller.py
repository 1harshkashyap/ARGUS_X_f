from app.sentience.state import GlobalState
from app.sentience.intent import SystemIntent
from app.sentience.monologue import Monologue

class SentienceController:
    def __init__(self):
        self.state = GlobalState()
        self.intent = SystemIntent()
        self.monologue = Monologue()

    def process(self, event):
        self.state.update(event)

        event.data["system_state"] = {
            "alert": self.state.alert_level,
            "focus": self.state.focus,
            "confidence": self.state.confidence
        }

        event.data["system_intent"] = self.intent.decide(event)

        event.data["monologue"] = self.monologue.generate(event)

        return event
