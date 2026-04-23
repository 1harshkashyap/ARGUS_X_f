class BlueAgent:
    def __init__(self):
        self.rules = []

    def defend(self, attack):
        for rule in self.rules:
            if rule in attack:
                return True
        return False

    def learn(self, result):
        # Learn from successful attacks (Red bypassed defense)
        if result["success"]:
            if result["attack"] not in self.rules:
                self.rules.append(result["attack"])
        
        if len(self.rules) > 20:
            self.rules = self.rules[-20:]
