class IntentEngine:

    def detect(self, text):

        if "ignore" in text.lower():
            return "Prompt Injection"

        if "reveal" in text.lower():
            return "Data Exfiltration"

        if "admin" in text.lower():
            return "Privilege Escalation"

        return "Unknown"
