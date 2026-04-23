from app.ml.embedding_engine import EmbeddingEngine

class EmbeddingProcessor:
    def __init__(self):
        self.engine = EmbeddingEngine()

    def handle(self, event):
        score = self.engine.similarity(event.text, event.org_id)
        
        allowed = True
        threat_score = 0
        
        if score > 0.9:
            allowed = False
            threat_score = 7

        if not allowed:
            self.engine.add(event.text, event.org_id)
            
        return {
            "similarity_score": score,
            "allowed": allowed,
            "threat_score": threat_score
        }
