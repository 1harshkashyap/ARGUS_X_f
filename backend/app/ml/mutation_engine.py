class MutationEngine:
    def generate_variants(self, text: str) -> list[str]:
        return [
            text,
            text.lower(),
            text.upper(),
            text.replace(" ", "_"),
            "please " + text,
            text + " now",
        ]
