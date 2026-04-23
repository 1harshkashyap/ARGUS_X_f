from app.intelligence.metrics import Metrics
from app.intelligence.strategy import StrategyEngine
from app.intelligence.thought_engine import ThoughtEngine
from app.intelligence.narrative import NarrativeEngine
from app.intelligence.intent import IntentEngine

class IntelligenceController:
    def __init__(self):
        self.metrics = Metrics()
        self.strategy = StrategyEngine()
        self.thoughts = ThoughtEngine()
        self.narrative = NarrativeEngine()
        self.intent = IntentEngine()

    def process(self, event):
        self.metrics.update(event)
        mode = self.strategy.update(self.metrics)

        # Inject metrics, mode, and thoughts into event
        event.data["block_rate"] = self.metrics.block_rate()
        event.data["avg_threat"] = self.metrics.avg_threat()
        event.data["mode"] = mode
        event.data["thoughts"] = self.thoughts.generate(event)
        event.data["narrative"] = self.narrative.generate(event)
        event.data["intent"] = self.intent.detect(event.text)

        return event
