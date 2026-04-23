from app.ml.auditor import OutputAuditor

class AuditProcessor:
    def __init__(self):
        self.auditor = OutputAuditor()

    def handle(self, event):
        response = "Request processed" if event.allowed else "Blocked"

        response, flagged = self.auditor.audit(response)

        return {
            "response": response,
            "flagged": flagged
        }
