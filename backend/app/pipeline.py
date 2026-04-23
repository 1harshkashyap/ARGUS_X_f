import asyncio
from app.ml.embedding_engine import EmbeddingEngine


class SecurityPipeline:
    def __init__(
        self,
        firewall,
        fingerprinter,
        auditor,
        mutation_engine,
        xai,
        evolution,
        correlator,
        supabase,
    ):
        self.firewall = firewall
        self.fingerprinter = fingerprinter
        self.auditor = auditor
        self.mutation_engine = mutation_engine
        self.xai = xai
        self.evolution = evolution
        self.correlator = correlator
        self.supabase = supabase
        self.embedding = EmbeddingEngine()

    async def process(self, text: str, org_id: str) -> dict:
        allowed = self.firewall.check_input(text)

        similarity_score = self.embedding.similarity(text, org_id)
        fingerprint = self.fingerprinter.fingerprint(text)
        
        threat_score = 7 if not allowed else 1
        
        if similarity_score > 0.9:
            allowed = False
            threat_score = 7
        elif similarity_score > 0.75:
            threat_score = max(threat_score, 6)

        try:
            await asyncio.to_thread(
                lambda: self.supabase.table("attack_logs").insert({
                    "org_id": org_id,
                    "input_text": text,
                    "allowed": allowed,
                    "fingerprint": fingerprint,
                    "threat_score": threat_score,
                }).execute()
            )
        except Exception:
            pass

        variants = self.mutation_engine.generate_variants(text)
        for variant in variants:
            _ = self.firewall.check_input(variant)

        if allowed:
            response_text = "Request processed successfully."
        else:
            response_text = "Request blocked by security system."
        response_text, flagged = self.auditor.audit(response_text)
        reason = self.xai.explain(text, allowed)
        evolution_score = self.evolution.compute_score(text)
        correlation_count = await asyncio.to_thread(
            self.correlator.correlate, fingerprint
        )

        if correlation_count > 5:
            threat_score = min(10, threat_score + 2)

        if evolution_score > 6:
            threat_score = min(10, threat_score + 1)

        if not allowed:
            self.embedding.add(text, org_id)

        return {
            "allowed": allowed,
            "fingerprint": fingerprint,
            "threat_score": threat_score,
            "response": response_text,
            "flagged": flagged,
            "reason": reason,
            "evolution_score": evolution_score,
            "correlation_count": correlation_count,
        }
