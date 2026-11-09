import json
from pathlib import Path


class TextFileStorage:
    def __init__(self, file_path=None):
        if file_path is None:
            project_folder = Path(__file__).resolve().parent.parent
            file_path = project_folder / "data" / "healthcare_data.txt"
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
