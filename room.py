import numpy as np
import json

class Room:
    def __init__(self, name, width, height, door=None):
        self.name = name
        self.width = width
        self.height = height
        self.initial_grid = np.zeros((height, width))  # Grille vide (0 = libre)
        
        # Positionner la porte
        self.door = door
        if door:
            self.initial_grid[door['x'], door['y']] = -1  # Marque la porte sur la grille (-1)
        
        self.grid = self.initial_grid.copy()  # Grille actuelle

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

    def can_place_furniture(self, x, y, furniture):
        """Alias de is_position_valid pour vérifier si un meuble peut être placé."""
        return self.is_position_valid(x, y, furniture)

    def place_furniture(self, x, y, furniture):
        """Place un meuble dans la pièce si possible."""
        if self.can_place_furniture(x, y, furniture):
            self.grid[x:x+furniture.height, y:y+furniture.width] = 1
            return True
        return False

    def reset_grid(self):
        """Réinitialise la grille à son état initial."""
        self.grid = self.initial_grid.copy()