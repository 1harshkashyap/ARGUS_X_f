from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os

class EmbeddingEngine:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384
        self.indices = {}

    def _get_index(self, org_id: str):
        if org_id not in self.indices:
            index_file = f"faiss_{org_id}.index"
            if os.path.exists(index_file):
                self.indices[org_id] = faiss.read_index(index_file)
            else:
                self.indices[org_id] = faiss.IndexFlatL2(self.dimension)
        return self.indices[org_id]

    def embed(self, text: str):
        emb = self.model.encode(text)
        return np.array([emb]).astype("float32")

    def add(self, text: str, org_id: str):
        vec = self.embed(text)
        index = self._get_index(org_id)
        index.add(vec)
        faiss.write_index(index, f"faiss_{org_id}.index")

    def similarity(self, text: str, org_id: str) -> float:
        index = self._get_index(org_id)
        if index.ntotal == 0:
            return 0.0

        query = self.embed(text)
        distances, _ = index.search(query, 1)

        # Convert L2 distance to similarity score
        distance = distances[0][0]
        similarity = 1 / (1 + distance)

        return float(similarity)
