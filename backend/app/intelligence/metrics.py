class Metrics:
    def __init__(self):
        self.total_requests = 0
        self.blocked_requests = 0
        self.total_threat_score = 0

    def update(self, event):
        self.total_requests += 1

        if not event.allowed:
            self.blocked_requests += 1

        self.total_threat_score += event.threat_score

    def block_rate(self):
        if self.total_requests == 0:
            return 0.0
        return self.blocked_requests / self.total_requests

    def avg_threat(self):
        if self.total_requests == 0:
            return 0.0
        return self.total_threat_score / self.total_requests
