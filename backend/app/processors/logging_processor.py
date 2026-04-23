from app.db.supabase_client import get_supabase

class LoggingProcessor:
    def __init__(self):
        self.supabase = get_supabase()

    def handle(self, event):
        try:
            self.supabase.table("attack_logs").insert({
                "input_text": event.text,
                "allowed": event.allowed,
                "fingerprint": event.data.get("fingerprint"),
                "threat_score": event.threat_score,
                "org_id": event.org_id
            }).execute()
        except Exception as e:
            print("Supabase logging failed:", e)
