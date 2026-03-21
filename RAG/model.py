import os
import numpy as np
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import faiss
import pickle
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

HF_TOKEN = os.getenv("API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

try:
    from RAG.data_retriever import retrieve
except ImportError:
    from data_retriever import retrieve

# -------------------------------
# 🤖 Generate Answer (Groq via LangChain)
# -------------------------------
def generate_answer(query):
    docs = retrieve(query)
    context = "\n\n".join([doc["content"] for doc in docs])

    # Initialize Groq LLM via LangChain
    groq_llm = init_chat_model(
        model="llama-3.1-8b-instant",
        model_provider="groq",
        api_key=GROQ_API_KEY
    )

    # Create messages for the chat model
    messages = [
        SystemMessage(content="Answer based only on the provided context."),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
    ]

    # Generate response
    response = groq_llm.invoke(messages)
    answer = response.content  # LangChain chat_models returns an object with .content

    return answer, docs


# -------------------------------
# 🚀 Test
# -------------------------------
if __name__ == "__main__":
    query = "What is machine learning?"

    answer, sources = generate_answer(query)

    print("\n🤖 Answer:\n", answer)

    print("\n📄 Sources:")
    for i, doc in enumerate(sources):
        print(f"\n🔹 Source {i+1}")
        print(doc["content"][:200])