from app.ml.mutation_engine import MutationEngine

class MutationProcessor:
    def __init__(self):
        self.engine = MutationEngine()

    def handle(self, event):
        variants = self.engine.generate_variants(event.text)

        # Passive stress testing (no patching, no logging)
        for variant in variants:
            try:
                _ = variant  # placeholder (no firewall call to avoid side effects)
            except:
                pass
                
        event.data["mutation_count"] = len(variants)
