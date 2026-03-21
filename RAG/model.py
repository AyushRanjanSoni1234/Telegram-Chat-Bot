import os
import json
import numpy as np
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import faiss
import pickle
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

try:
    from RAG.memory import QuestionMemory
except ImportError:
    from memory import QuestionMemory

load_dotenv()

HF_TOKEN = os.getenv("API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize memory
memory = QuestionMemory()

try:
    from RAG.data_retriever import retrieve
except ImportError:
    from data_retriever import retrieve

# -------------------------------
# 🤖 Generate Answer (Groq via LangChain)
# -------------------------------
def generate_answer(query):
    # 1. Check Memory (Cache) first
    cached_answer = memory.get_answer(query)
    if cached_answer:
        # If it's cached, it should already be the structured dict or string
        # We'll return it and indicate it was from memory
        if isinstance(cached_answer, str):
            try:
                cached_answer = json.loads(cached_answer)
            except:
                pass
        return cached_answer, []

    docs = retrieve(query)
    context = "\n\n".join([doc["content"] for doc in docs])

    # Initialize Groq LLM via Langchain
    groq_llm = init_chat_model(
        model="llama-3.1-8b-instant", # Using the known-valid model
        model_provider="groq",
        api_key=GROQ_API_KEY,
        model_kwargs={"response_format": {"type": "json_object"}}
    )

    # Create messages for the chat model
    system_prompt = (
        "You are a helpful assistant. Answer based only on the provided context. "
        "Your response MUST be a valid JSON object with these keys:\n"
        "- 'answer': Detailed answer string.\n"
        "- 'confidence': Float score 0-1.\n"
        "- 'category': Short label (e.g., 'Technical', 'General', 'Info')."
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
    ]

    # Generate response
    try:
        response = groq_llm.invoke(messages)
        res_text = response.content
        
        # Parse JSON
        try:
            structured_res = json.loads(res_text)
        except json.JSONDecodeError:
            # Fallback for non-JSON response
            structured_res = {
                "answer": res_text,
                "confidence": 0.5,
                "category": "Uncategorized"
            }

        # Save to memory
        memory.save_answer(query, structured_res)

        return structured_res, docs
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "confidence": 0, "category": "Error"}, []


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