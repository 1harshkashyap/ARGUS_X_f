class JudgeAgent:
    def evaluate(self, attack, defended):
        success = not defended

        score = 1 if success else 0

        return {
            "attack": attack,
            "success": success,
            "score": score
        }
