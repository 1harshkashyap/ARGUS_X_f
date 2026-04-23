import random

class BattleEngine:
    def __init__(self, firewall, red_agent, blue_agent):
        self.firewall = firewall
        self.red_agent = red_agent
        self.blue_agent = blue_agent
        self.attack_count = 0
        self.bypass_count = 0

    def run_cycle(self, mode: str = "normal") -> dict:
        if mode == "relaxed" and random.random() < 0.5:
            return {"status": "skipped", "mode": mode}

        cycles = 2 if mode == "aggressive" else 1
        
        last_result = None
        for _ in range(cycles):
            res = self.red_agent.run()
            attack = res["attack"]
            allowed = res["allowed"]

            self.attack_count += 1

            if allowed:
                self.bypass_count += 1
                self.blue_agent.apply_patch(attack)

            block_rate = 1 - (self.bypass_count / self.attack_count)

            last_result = {
                "attack": attack,
                "allowed": allowed,
                "attack_count": self.attack_count,
                "bypass_count": self.bypass_count,
                "block_rate": block_rate,
                "mode": mode
            }

        return last_result
