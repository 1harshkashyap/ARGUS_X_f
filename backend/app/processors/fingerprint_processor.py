from app.ml.fingerprinter import Fingerprinter

class FingerprintProcessor:
    def __init__(self):
        self.fp = Fingerprinter()

    def handle(self, event):
        event.data["fingerprint"] = self.fp.fingerprint(event.text)
