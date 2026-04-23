class Fingerprinter:
    def fingerprint(self, text: str) -> str:
        return str(abs(hash(text)))
