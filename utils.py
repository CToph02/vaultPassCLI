#Utils for Json
import json

class jsonUtils():

    def __init__(self):
        self.pwd = {}

    def load_json(self, jsonFile: json) -> json:
        try:
            with open(jsonFile,"r") as j:
                return json.load(j)

        except FileNotFoundError:
            return self.pwd

    def save_json(self, jsonFile: json, data: dict) -> json:
        try:
            with open(jsonFile, "w") as j:
                json.dump(data, j, indent=4) 
        except Exception as e:
            return f"No se pudo guardar el archivo. Error {e}"