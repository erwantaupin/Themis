import numpy as np
import json

class Room:
    def __init__(self, name, width, height, door=None):
        self.name = name
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))  # Grille vide (0 = libre)
        
        # Positionner la porte
        self.door = door
        if door:
            self.grid[door['x'], door['y']] = -1  # Marque la porte sur la grille (-1)

    @classmethod
    def from_json(cls, filepath):
        """Charge une pièce depuis un fichier JSON."""
        with open(filepath, 'r') as file:
            data = json.load(file)
        return cls(data["name"], data["width"], data["height"], data.get("door"))

    def is_position_valid(self, x, y, furniture):
        """Vérifie si une position est valide pour un meuble."""
        if x + furniture.height > self.height or y + furniture.width > self.width:
            return False  # Hors des limites
        return np.all(self.grid[x:x+furniture.height, y:y+furniture.width] == 0)

    def place_furniture(self, x, y, furniture):
        """Place un meuble dans la pièce si possible."""
        if self.is_position_valid(x, y, furniture):
            self.grid[x:x+furniture.height, y:y+furniture.width] = 1
            return True
        return False