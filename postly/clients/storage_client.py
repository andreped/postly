import json
from typing import Dict, Any


class StorageClient:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._load_data()

    def _load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {"users": {}, "posts": []}

    def _save_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_data(self) -> Dict[str, Any]:
        return self.data

    def update_data(self, data: Dict[str, Any]):
        self.data = data
        self._save_data()
