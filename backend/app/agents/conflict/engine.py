from app.agents.conflict.red_agent import RedAgent
from app.agents.conflict.blue_agent import BlueAgent
from app.agents.conflict.judge_agent import JudgeAgent
from app.agents.conflict.architect_agent import ArchitectAgent

class ConflictEngine:
    def __init__(self):
        self.red = RedAgent()
        self.blue = BlueAgent()
        self.judge = JudgeAgent()
        self.architect = ArchitectAgent()

    def run_cycle(self):
        attack = self.red.act()

        defended = self.blue.defend(attack)

        result = self.judge.evaluate(attack, defended)

        self.red.learn(result)
        self.blue.learn(result)

        strategy = self.architect.update(result)

        return {
            "attack": attack,
            "defended": defended,
            "result": result,
            "strategy": strategy,
            "learning": {
                "red_policy": self.red.get_learning_state(),
                "blue_policy": self.blue.get_learning_state()
            },
            "prediction": self.red.get_learning_state()
        }
