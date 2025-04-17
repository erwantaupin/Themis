from room import Room
from furniture import Furniture
from ai_trainer import PlacementAI
from visualizer import Visualizer


def main():
    # Définir une pièce de 45 m² (9m x 5m)
    room = Room(name="Living Room", width=9, height=5)
    room.add_door(1, 0)
    room.add_window(0, 4)

    # Liste des meubles
    furniture_list = [
        Furniture("Canapé", 2, 1, "gray", "sofa"),
        Furniture("Table basse", 1, 1, "brown", "table"),
        Furniture("Bureau", 2, 1, "black", "desk"),
        Furniture("Chaise", 1, 1, "white", "chair"),
        Furniture("Télévision", 1, 1, "black", "electronics"),
    ]

    room.reset_grid()

    # Créer et charger/enregistrer l'IA
    placement_ai = PlacementAI(room, furniture_list)

    # Entraîner l'IA si nécessaire
    best_placements = placement_ai.train(episodes=100)

    # Enregistrer et tester à partir du modèle sauvegardé
    test_placements = placement_ai.predict()

    # Affichage des scores
    print("Meilleur score final :", placement_ai.best_score)
    print("Score final de l'aménagement :", placement_ai.current_score)
    print("Placements de test :", [(f.name, x, y) for f, x, y in test_placements])

    # Visualiser le meilleur aménagement issu du test
    visualizer = Visualizer(room, test_placements)
    visualizer.visualize()

if __name__ == "__main__":
    main()
