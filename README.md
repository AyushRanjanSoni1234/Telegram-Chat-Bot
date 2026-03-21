# 🤖 GenAI RAG Telegram Bot

Welcome to the **GenAI RAG Telegram Bot**! This project is an intelligent chat assistant built on Telegram that uses **Retrieval-Augmented Generation (RAG)** to answer user questions based on your own custom documents. 

Instead of relying solely on an LLM's pre-trained knowledge, this bot first searches through your provided knowledge base, retrieves the most relevant information, and then formulates a highly accurate, context-aware answer. 

---

## ✨ Features

- **Multi-Format Document Support**: Seamlessly read and ingest data from `.pdf`, `.docx`, `.csv`, `.txt`, and `.json` files.
- **Fast & Lightweight Embeddings**: Uses the HuggingFace Inference API (`sentence-transformers/all-MiniLM-L6-v2`) to generate text embeddings without relying on heavy local computational resources (No local PyTorch required!).
- **Vector Database**: Utilizes **FAISS (Facebook AI Similarity Search)** to quickly search and retrieve relevant information from thousands of documents.
- **Lightning-Fast LLM**: Powered by **Groq**'s ultra-fast API running the `llama-3.1-8b-instant` model to craft human-like answers.
- **Accessible Interface**: Built directly into Telegram as a conversational bot for an easy and portable user experience.

---

## 📂 Project Structure

Here is a human-readable breakdown of how the project is organized:

```text
📦 GENAI_BOT
├── 📁 Data/                  # 📄 Put all your raw documents here (PDFs, Word Docs, TXTs, etc.)
├── 📁 db/                    # 🧠 The generated FAISS vector database (created automatically)
├── 📁 RAG/                   # ⚙️ The core logic engine driving the bot
│   ├── data_ingestion.py     # 📥 Reads 'Data/', chunks text, gets embeddings, and saves to 'db/'
│   ├── data_retriever.py     # 🔍 Loads the 'db/' and finds the most relevant chunks for a question
│   └── model.py              # 🧠 Combines the retrieved data with Groq's LLM to generate answers
├── 📄 app.py                 # 🚀 The main Telegram Bot entry point (Run this to start!)
├── 📄 .env                   # 🔑 Environment variables (API Keys and Tokens)
├── 📄 pyproject.toml         # 📦 `uv` dependency & package manager configuration
└── 📄 requirements.txt       # 📌 Standard Python dependencies list
```

---

## 🛠️ How it Works

1. **Ingestion (`data_ingestion.py`)**: The script loops through everything in your `Data/` folder. It cuts large documents into bite-sized chunks to make them easily searchable.
2. **Embedding**: We take those text chunks and ask HuggingFace to translate them into numbers (vectors/embeddings).
3. **Indexing (`db/`)**: The vectors are saved into a FAISS index, acting as the bot's "long-term memory".
4. **User Queries (`app.py` & `model.py`)**: When you message the bot on Telegram `/ask <question>`, the bot converts your question into a vector and searches the FAISS memory.
5. **Generation**: Groq's `llama-3` looks at the search results and formulates a smart, accurate response to send back to you!

---

## 🚀 Setup & Execution Guide

### 1. Requirements

Ensure you have your environment set up. We recommend using `uv` for lightning-fast package management:

```bash
# Using uv (recommended)
uv sync

# Or using standard pip
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory and add your API keys:

```ini
TELEGRAM_TOKEN=your_telegram_bot_token_here
API_KEY=your_huggingface_access_token
GROQ_API_KEY=your_groq_api_key
```

### 3. Add Your Data

Drop any files you want the bot to "read" into the `Data/` folder. (PDFs, Word documents, CSVs, etc.).

### 4. Create the Knowledge Base (Index)

Run the data ingestion script so the AI can read and memorize your documents:

```bash
uv run python RAG/data_ingestion.py
```
*(Note: If you are running on Windows and see emoji encoding errors in the terminal, you can prefix the command with `$env:PYTHONIOENCODING="utf-8";` in PowerShell).*

### 5. Start the Bot!

Fire up the Telegram bot:

```bash
uv run python app.py
```

Go to Telegram, find your bot, hit `/start`, and use `/ask What is my document about?` to start chatting! 🎉
