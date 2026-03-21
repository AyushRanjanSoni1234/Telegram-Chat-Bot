# 🤖 GenAI RAG Telegram Bot (Python 3.14 Optimized)

Welcome to the **GenAI RAG Telegram Bot**! This is a state-of-the-art intelligent assistant built for Telegram that uses **Retrieval-Augmented Generation (RAG)** to answer questions based on your custom documents.

This version has been specifically engineered to run on **Python 3.14** and Windows, featuring advanced memory caching and structured AI outputs.

---

## ✨ Core Features

- **📂 Multi-Format Ingestion**: Supports `.pdf`, `.docx`, `.csv`, `.txt`, and `.json`.
- **🚀 Ultra-Fast RAG**: Powered by **Groq** (`llama-3.1-8b-instant`) and **FAISS** for near-instant retrieval and answering.
- **💾 Smart Memory (Caching)**: Remembers previous questions. If you ask the same thing twice, it responds instantly from local memory (`db/memory.json`) to save API credits.
- **📊 Structured Responses**: Every answer includes a **Confidence Score** and **Category Label** for a professional, structured feel.
- **🐍 Python 3.14 Ready**: Custom "Monkey-Patching" and "Lazy Loading" logic to handle PyTorch/Transformers DLL compatibility issues on the latest Python versions.
- **📷 Vision Support**: Can detect text in images (OCR) and generate descriptions (Captioning).

---

## 📂 Project Structure

```text
📦 GENAI_BOT
├── 📁 Data/                  # 📄 Raw documents for the bot to read
├── 📁 db/                    # 🧠 FAISS Vector Index & memory.json cache
├── 📁 RAG/                   # ⚙️ Core AI Engine
│   ├── memory.py             # 💾 (NEW) Persistent Q&A Caching logic
│   ├── data_ingestion.py     # 📥 Document processor & embedder
│   ├── data_retriever.py     # 🔍 Semantic search functionality
│   └── model.py              # 🧠 LLM integration with structured JSON output
├── 📁 Vision/                # 📷 Image processing (OCR & Captioning)
├── 📄 main.py                # 🚀 RECOMMENDED ENTRY POINT (with 3.14 fixes)
├── 📄 app.py                 # 🤖 Telegram Bot handler logic
├── 📄 .env                   # 🔑 Your API Keys (Groq, HF, Telegram)
└── 📄 requirements.txt       # 📌 Project dependencies
```

---

## 🛠️ Step-by-Step Setup

### 1. Install Dependencies
We recommend using `uv` for the fastest setup on Windows/Python 3.14:
```powershell
uv sync
# OR
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file in the root directory:
```ini
TELEGRAM_TOKEN=8683560980:AAE2O5nRq2W3VBOgu52qF7CByMHkkVgiCjc
GROQ_API_KEY=your_groq_key_here
API_KEY=your_huggingface_token_here
```

### 3. Ingest Your Data
Place your documents in the `Data/` folder, then run:
```powershell
uv run python RAG/data_ingestion.py
```

### 4. Start the Bot
Always use **`main.py`** to start the bot. It contains critical stability fixes for Python 3.14:
```powershell
uv run python main.py
```

---

## 💡 How to Use
- **Text Questions**: Use `/ask <your question>` or just send a message.
- **Image Input**: Send an image, and the bot will analyze the contents before answering.
- **Repeat Questions**: Notice the `💾 [FROM MEMORY]` tag when you ask a question you've asked before!

---

## 🛡️ Technical Stability Note (Python 3.14)
If you are running on Windows with Python 3.14, standard PyTorch/Transformers DLLs often fail to initialize (`WinError 1114`). 

**Fixed in this project:**
- We use a "Mocking" strategy in `main.py` that allows the RAG system (Text) to function perfectly even if the heavy Vision DLLs fail to load.
- All vision features are **lazily loaded**, meaning the bot won't crash on startup if vision is temporarily unavailable.
