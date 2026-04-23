from app.ml.firewall import firewall

class FirewallProcessor:
    def __init__(self):
        self.firewall = firewall

    def handle(self, event):
        allowed = self.firewall.check_input(event.text)
        event.allowed = allowed

        if not allowed:
            event.threat_score = max(event.threat_score, 7)
