class ArchitectAgent:
    def __init__(self):
        self.strategy_log = []

    def update(self, result):
        if result["success"]:
            decision = "Red exploited weakness"
        else:
            decision = "Blue successfully defended"

        self.strategy_log.append(decision)

        return decision
