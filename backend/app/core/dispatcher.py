from app.core.event_bus import EventBus
from app.processors.firewall_processor import FirewallProcessor
from app.processors.fingerprint_processor import FingerprintProcessor
from app.processors.audit_processor import AuditProcessor
from app.processors.embedding_processor import EmbeddingProcessor
from app.processors.xai_processor import XAIProcessor
from app.processors.evolution_processor import EvolutionProcessor
from app.processors.correlation_processor import CorrelationProcessor
from app.processors.logging_processor import LoggingProcessor
from app.processors.mutation_processor import MutationProcessor
from app.intelligence.controller import IntelligenceController
from app.sentience.controller import SentienceController

class Dispatcher:
    def __init__(self):
        self.bus = EventBus()
        self.intelligence = IntelligenceController()
        self.sentience = SentienceController()
        
        self.bus.register(FirewallProcessor(), "critical")
        self.bus.register(FingerprintProcessor(), "critical")

        self.bus.register(MutationProcessor(), "background")
        self.bus.register(EmbeddingProcessor(), "parallel")
        self.bus.register(EvolutionProcessor(), "parallel")
        self.bus.register(CorrelationProcessor(), "parallel")
        self.bus.register(XAIProcessor(), "parallel")

        self.bus.register(AuditProcessor(), "critical")
        self.bus.register(LoggingProcessor(), "background")

    async def dispatch(self, event, broadcaster=None):
        event = await self.bus.process(event)

        event = self.intelligence.process(event)
        event = self.sentience.process(event)

        if broadcaster:
            try:
                broadcaster(event)
            except:
                pass

        return event
