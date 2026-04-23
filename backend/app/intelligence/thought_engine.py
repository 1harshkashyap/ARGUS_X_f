class ThoughtEngine:

    def generate(self, event):

        thoughts = []

        if not event.allowed:
            thoughts.append("⚠️ Suspicious pattern detected")

        if event.threat_score > 7:
            thoughts.append("🔥 High threat level — immediate action")

        if event.data.get("similarity_score", 0) > 0.8:
            thoughts.append("🧠 Similar to known attack pattern")

        if event.data.get("correlation_count", 0) > 3:
            thoughts.append("🔗 Part of ongoing attack sequence")

        return thoughts
