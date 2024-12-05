from room import Room
from furniture import Furniture
from ai_trainer import PlacementAI
from visualizer import Visualizer
import numpy as np

def main():
    # Charger les données depuis les fichiers JSON
    room = Room.from_json("data/room.json")
    wallet = Furniture.from_json("data/furniture.json")

    # Initialisation de l'IA
    placement_ai = PlacementAI(room, wallet)

    # Entraîner l'IA
    best_placements = placement_ai.train(epochs=100)

    # Afficher le résultat
    visualizer = Visualizer(room, best_placements)
    visualizer.display_room()

if __name__ == "__main__":
    main()