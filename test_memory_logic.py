import sys
import os
from unittest.mock import MagicMock

# 1. 3.14 Compatibility Patch (same as main.py)
if sys.version_info >= (3, 14) and os.name == 'nt':
    sys.modules['torch'] = MagicMock()
    sys.modules['transformers'] = MagicMock()
    sys.modules['easyocr'] = MagicMock()

from RAG.model import generate_answer

def test_flow():
    query = "What is the role of this AI bot?"
    
    print(f"--- First Call for: '{query}' ---")
    res1, docs1 = generate_answer(query)
    print("Response 1:", res1)
    
    print(f"\n--- Second Call for: '{query}' (Should be from Memory) ---")
    res2, docs2 = generate_answer(query)
    print("Response 2:", res2)
    
    if res1 == res2 and not docs2:
        print("\n[OK] SUCCESS: Memory cache worked!")
    else:
        print("\n[FAIL] FAILURE: Memory cache did not return expected result.")

if __name__ == "__main__":
    test_flow()
