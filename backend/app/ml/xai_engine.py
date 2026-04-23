class XAIEngine:
    def explain(self, text: str, allowed: bool) -> str:
        if allowed:
            return "Input passed all security checks."
        return "Input blocked due to suspicious pattern detection."
