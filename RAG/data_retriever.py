import os
import numpy as np
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings  # ✅ FIX

load_dotenv()
HF_TOKEN = os.getenv("API_KEY")


# -------------------------------
# 🔥 FIXED Embedding Class
# -------------------------------
class HFEmbedding(Embeddings):  # ✅ FIX (inherit)

    def __init__(self, token):
        self.client = InferenceClient(token=token)
        self.model = "sentence-transformers/all-MiniLM-L6-v2"

    def embed_query(self, text: str) -> list[float]:
        try:
            emb = self.client.feature_extraction(text, model=self.model)

            # ✅ handle empty response
            if emb is None or len(emb) == 0:
                return [0.0] * 384

            vector = np.array(emb, dtype="float32")

            if vector is None or len(vector) == 0:
                return [0.0] * 384

            return vector.tolist()

        except Exception as e:
            print(f"❌ Embedding error: {e}")
            return [0.0] * 384

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(t) for t in texts if t.strip()]

    # ✅🔥 CRITICAL FIX (makes FAISS work)
    def __call__(self, text: str) -> list[float]:
        return self.embed_query(text)


# -------------------------------
# 🔍 Load Retriever
# -------------------------------
def get_retriever():

    embedding = HFEmbedding(token=HF_TOKEN)

    db = FAISS.load_local(
        "db",
        embedding,
        allow_dangerous_deserialization=True
    )

    return db.as_retriever(search_kwargs={"k": 3})


# -------------------------------
# 🔎 Retrieve Function
# -------------------------------
def retrieve(query):
    retriever = get_retriever()

    docs = retriever.invoke(query)  # ✅ new API

    return [
        {
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown")
        }
        for doc in docs
    ]


# -------------------------------
# 🚀 Test
# -------------------------------
if __name__ == "__main__":
    query = "What is role we work in different comapny?"

    results = retrieve(query)

    for i, res in enumerate(results):
        print(f"\n🔹 Result {i+1}")
        print("Source:", res["source"])
        print("Content:", res["content"][:200])