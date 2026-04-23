from app.db.supabase_client import get_supabase


class ThreatCorrelator:
    def __init__(self):
        self.supabase = get_supabase()

    def correlate(self, fingerprint: str) -> int:
        response = (
            self.supabase
            .table("attack_logs")
            .select("id")
            .eq("fingerprint", fingerprint)
            .execute()
        )
        count = len(response.data)
        return count
