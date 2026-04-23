class OutputAuditor:
    BLOCKED_PATTERNS = [
        "system prompt",
        "internal config",
        "api key",
        "secret",
    ]

    def audit(self, text: str) -> tuple[str, bool]:
        lowered = text.lower()
        for pattern in self.BLOCKED_PATTERNS:
            if pattern in lowered:
                return "Response blocked by security policy.", True
        return text, False
