import sys
import os

# 🔥 Python 3.14 Compatibility Hack
# On Windows + Python 3.14, PyTorch DLLs often fail to load (WinError 1114).
# We mock these modules so RAG/LangChain can start without crashing.
if sys.version_info >= (3, 14) and os.name == 'nt':
    from unittest.mock import MagicMock
    sys.modules['torch'] = MagicMock()
    sys.modules['transformers'] = MagicMock()
    sys.modules['easyocr'] = MagicMock()

import app
try:
    from RAG.data_ingestion import create_index
except ImportError:
    from data_ingestion import create_index

def main():
    print("Starting GenAI Telegram Bot...")
    create_index()
    app.main()

if __name__ == "__main__":
    main()
