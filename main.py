from room import Room
from furniture import Furniture
from ai_trainer import PlacementAI
from visualizer import Visualizer
from evaluator import Evaluator  # Ajout de l'import

def main():
    # Charger les données depuis les fichiers JSON
    room = Room.from_json("data/room.json")
    wallet = Furniture.from_json("data/furniture.json")

    # Initialisation de l'IA et de l'évaluateur
    placement_ai = PlacementAI(room, wallet)
    evaluator = Evaluator(room, wallet)

    # Entraîner l'IA
    best_placements = placement_ai.train(iterations=100)

    # Évaluer le résultat final
    final_score = evaluator.evaluate()
    print(f"Score final de l'aménagement : {final_score}")

    # Afficher la disposition
    visualizer = Visualizer(room, best_placements)
    visualizer.display_room()

if __name__ == "__main__":
    main()