from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

class JobRecommender:
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                 index_path="embeddings/faiss_index.bin"):
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.job_texts = []
        self.index = None

    def build_index(self, job_descriptions):
        self.job_texts = job_descriptions
        embeddings = self.model.encode(job_descriptions, show_progress_bar=True)
        dim = embeddings[0].shape[0]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings).astype("float32"))
        faiss.write_index(self.index, self.index_path)
        with open("embeddings/job_texts.pkl", "wb") as f:
            pickle.dump(self.job_texts, f)

    def load_index(self):
        self.index = faiss.read_index(self.index_path)
        with open("embeddings/job_texts.pkl", "rb") as f:
            self.job_texts = pickle.load(f)

    def recommend(self, cv_text, top_k=5):
        query = self.model.encode([cv_text])
        distances, indices = self.index.search(np.array(query), top_k)
        return [(self.job_texts[i], distances[0][j]) for j, i in enumerate(indices[0])]