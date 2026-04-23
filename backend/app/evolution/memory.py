class EvolutionMemory:
    def __init__(self):
        self.history = []

    def store(self, analysis):
        self.history.append(analysis)

        # keep last 50
        self.history = self.history[-50:]
