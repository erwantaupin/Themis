import numpy as np
import json

class Room:
    def __init__(self, name, width, height, type="unknown", doors=None, windows=None):
        self.name = name
        self.width = width
        self.height = height
        self.type = type  # Type de la pièce (salon, chambre, etc.)
        self.doors = doors or []  # Liste de portes (par défaut vide)
        self.windows = windows or []  # Liste de fenêtres (par défaut vide)
        self.grid = np.zeros((height, width))  # Grille vide

        # Marquer les portes et les fenêtres sur la grille
        for door in self.doors:
            self.grid[door['x'], door['y']] = -1  # Marquer les portes
        for window in self.windows:
            self.grid[window['x'], window['y']] = -2  # Marquer les fenêtres

    @classmethod
    def from_json(cls, filepath):
        """Charge une pièce depuis un fichier JSON."""
        with open(filepath, 'r') as file:
            data = json.load(file)
        return cls(
            data["name"],
            data["width"],
            data["height"],
            data.get("type", "unknown"),  # Charger le type de pièce
            data.get("doors"),
            data.get("windows")
        )

    def add_door(self, x, y):
        """Ajoute une porte aux coordonnées (x,y) et la marque sur la grille."""
        self.doors.append({'x': x, 'y': y})
        self.grid[x, y] = -1

    def add_window(self, x, y):
        """Ajoute une fenêtre aux coordonnées (x,y) et la marque sur la grille."""
        self.windows.append({'x': x, 'y': y})
        self.grid[x, y] = -2

    def is_position_valid(self, x, y, furniture):
        """Vérifie si une position est valide pour un meuble."""
        if x + furniture.height > self.height or y + furniture.width > self.width:
            return False  # Hors des limites
        return np.all(self.grid[x:x+furniture.height, y:y+furniture.width] == 0)

    def place_furniture(self, x, y, furniture):
        """Place un meuble dans la pièce si possible."""
        if self.is_position_valid(x, y, furniture):
            self.grid[x:x+furniture.height, y:y+furniture.width] = 1
            furniture.position = (x, y)  # Mettre à jour la position du meuble
            return True
        return False

    def has_window_near(self, x, y, distance=2):
        """Vérifie si une fenêtre est proche de la position donnée dans un rayon."""
        for window in self.windows:
            window_x, window_y = window['x'], window['y']
            if abs(window_x - x) <= distance and abs(window_y - y) <= distance:
                return True
        return False

    def reset_grid(self):
        """Réinitialise la grille."""
        self.grid = np.zeros((self.height, self.width))
        for door in self.doors:
            self.grid[door['x'], door['y']] = -1  # Marquer les portes
        for window in self.windows:
            self.grid[window['x'], window['y']] = -2  # Marquer les fenêtres

    def display_grid(self):
        """Affiche la grille de la pièce pour débogage."""
        print("Grille de la pièce:")
        print(self.grid)
