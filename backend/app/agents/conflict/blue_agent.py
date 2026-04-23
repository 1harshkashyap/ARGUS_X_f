import threading
from app.agents.conflict.beta_policy import BetaPolicy

class BlueAgent:
    def __init__(self):
        self.actions = [
            "ignore all instructions",
            "reveal system prompt",
            "bypass security restrictions",
            "act as admin"
        ]
        self.policy = BetaPolicy(self.actions)
        self.last_action = None
        self.load_state()

    def load_state(self):
        try:
            from app.db.supabase_client import get_supabase
            supabase = get_supabase()
            response = supabase.table("agent_state").select("state").eq("id", "blue").execute()
            if response.data and len(response.data) > 0:
                self.policy.from_dict(response.data[0]["state"])
        except Exception:
            pass

    def _save_task(self, state_dict):
        try:
            from app.db.supabase_client import get_supabase
            supabase = get_supabase()
            supabase.table("agent_state").upsert({
                "id": "blue",
                "state": state_dict
            }).execute()
        except Exception as e:
            print(f"[WARN] Persistence failed for BlueAgent: {e}")

    async def _save_state_async(self, state_dict):
        import asyncio
        await asyncio.to_thread(self._save_task, state_dict)

    def save_state(self):
        import asyncio
        state_dict = self.policy.to_dict()
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._save_state_async(state_dict))
        except RuntimeError:
            import threading
            threading.Thread(target=self._save_task, args=(state_dict,), daemon=True).start()

    def defend(self, attack):
        self.last_action = self.policy.sample()
        # Blue successfully defends if its selected posture matches the attack vector
        return self.last_action == attack

    def learn(self, result):
        # result["success"] means Red won, so Blue failed.
        # Blue wins if not result["success"].
        blue_success = not result["success"]
        self.policy.update(self.last_action, blue_success)
        self.save_state()

    def get_learning_state(self):
        return self.policy.get_probabilities()
