import os
import json
import hashlib

class QuestionMemory:
    def __init__(self, file_path="db/memory.json"):
        self.file_path = file_path
        self._ensure_dir()
        self.memory = self._load()

    def _ensure_dir(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=4)

    def _get_hash(self, question):
        # Normalize: lower case and strip whitespace, cast to string to be safe
        normalized = str(question).strip().lower()
        return hashlib.md5(normalized.encode("utf-8")).hexdigest()

    def get_answer(self, question):
        q_hash = self._get_hash(question)
        if q_hash in self.memory:
            return self.memory[q_hash]["answer"]
        return None

    def save_answer(self, question, answer):
        q_hash = self._get_hash(question)
        self.memory[q_hash] = {
            "question": question,
            "answer": answer
        }
        self._save()
