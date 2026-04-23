import re
from datetime import datetime

from app.db.supabase_client import get_supabase


class BlueAgent:
    def __init__(self, firewall):
        self.firewall = firewall
        self.supabase = get_supabase()
        self.rules = {}

    def generate_rule(self, text: str) -> str:
        return re.escape(text[:15])

    def apply_patch(self, text: str) -> None:
        pattern = self.generate_rule(text)

        if pattern in self.rules:
            self.rules[pattern] += 1
        else:
            self.rules[pattern] = 1

        if len(self.rules) > 50:
            least_used = min(self.rules, key=self.rules.get)
            del self.rules[least_used]

        existing = (
            self.supabase
            .table("dynamic_rules")
            .select("id")
            .eq("rule_pattern", pattern)
            .execute()
        )

        if existing.data:
            self.supabase.table("dynamic_rules").update({
                "patch_count": self.supabase.table("dynamic_rules")
                .select("patch_count")
                .eq("rule_pattern", pattern)
                .execute()
                .data[0]["patch_count"] + 1
            }).eq("rule_pattern", pattern).execute()
            return

        self.firewall.add_dynamic_rule(pattern)
        self.supabase.table("dynamic_rules").insert({
            "rule_pattern": pattern,
            "bypass_fingerprint": None,
            "created_at": datetime.utcnow().isoformat(),
            "active": True,
            "patch_count": 1,
        }).execute()
