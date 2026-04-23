class StrategyEngine:
    def __init__(self):
        self.mode = "normal"

    def update(self, metrics):
        block_rate = metrics.block_rate()

        if block_rate > 0.6:
            self.mode = "aggressive"
        elif block_rate < 0.2:
            self.mode = "relaxed"
        else:
            self.mode = "normal"

        return self.mode
