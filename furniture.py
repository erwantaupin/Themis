import json

class Furniture:
    def __init__(self, name, width, height, color, type):
        self.name = name
        self.width = width
        self.height = height
        self.color = color
        self.type = type

    @classmethod
    def from_json(cls, filepath):
        """Charge une liste de meubles depuis un fichier JSON."""
        with open(filepath, 'r') as file:
            data = json.load(file)
        return [cls(item["name"], item["width"], item["height"], item["color"], item["type"]) for item in data]