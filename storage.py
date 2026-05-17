import json


class Storage:
    FILE_NAME = "database.json"

    @staticmethod
    def save(data):
        with open(Storage.FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load():
        try:
            with open(Storage.FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "patients": [],
                "doctors": [],
                "appointments": [],
                "records": []
            }