from app.ml.xai_engine import XAIEngine

class XAIProcessor:
    def __init__(self):
        self.xai = XAIEngine()

    def handle(self, event):
        reason = self.xai.explain(event.text, event.allowed)
        return {
            "reason": reason
        }
