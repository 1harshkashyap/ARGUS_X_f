from app.agents.threat_correlator import ThreatCorrelator

class CorrelationProcessor:
    def __init__(self):
        self.correlator = ThreatCorrelator()

    def handle(self, event):
        fp = event.data.get("fingerprint")
        if not fp:
            return {}

        count = self.correlator.correlate(fp)
        
        return {
            "correlation_count": count,
            "threat_score_add": 2 if count > 5 else 0
        }
