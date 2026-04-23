import random

class BetaPolicy:
    def __init__(self, actions):
        self.actions = actions
        self.alphas = {a: 1.0 for a in actions}
        self.betas = {a: 1.0 for a in actions}

    def sample(self):
        best_action = None
        max_val = -1.0
        for a in self.actions:
            val = random.betavariate(self.alphas[a], self.betas[a])
            if val > max_val:
                max_val = val
                best_action = a
        return best_action

    def update(self, action, success):
        if success:
            self.alphas[action] += 1.0
        else:
            self.betas[action] += 1.0

    def get_probabilities(self):
        probs = {}
        for a in self.actions:
            alpha = self.alphas[a]
            beta = self.betas[a]
            probs[a] = round(alpha / (alpha + beta), 2)
        return probs

    def to_dict(self):
        return {
            "alphas": self.alphas,
            "betas": self.betas
        }

    def from_dict(self, data):
        if "alphas" in data:
            self.alphas = data["alphas"]
        if "betas" in data:
            self.betas = data["betas"]
