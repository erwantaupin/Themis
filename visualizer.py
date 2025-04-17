import os
import matplotlib.pyplot as plt
import numpy as np

class Visualizer:
    SAVE_DIR = "graph"

    def __init__(self, room, furniture_list):
        """Initialise le visualiseur avec la pièce et la liste de meubles ou de placements."""
        self.room = room
        if furniture_list and isinstance(furniture_list[0], tuple):
            # Extraire les objets Furniture s'ils sont dans des tuples (furniture, x, y)
            self.furniture_list = [f for f, *_ in furniture_list]
        else:
            self.furniture_list = furniture_list

    def visualize(self):
        """Affiche et sauvegarde la visualisation de la pièce et des meubles."""
        # Créer le dossier graph/ s'il n'existe pas
        os.makedirs(self.SAVE_DIR, exist_ok=True)

        # Créer la figure
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_aspect('equal')
        ax.set_xticks(np.arange(0, self.room.width + 1, 1))
        ax.set_yticks(np.arange(0, self.room.height + 1, 1))
        ax.grid(color='black', linestyle='-', linewidth=0.5)

        # Affichage des portes
        for door in self.room.doors:
            ax.add_patch(plt.Rectangle((door['y'], door['x']), 1, 1, color='blue', label='Porte'))
        # Affichage des fenêtres
        for window in self.room.windows:
            ax.add_patch(plt.Rectangle((window['y'], window['x']), 1, 1, color='cyan', label='Fenêtre'))

        # Affichage des meubles
        for furniture in self.furniture_list:
            if furniture.position is not None:
                x, y = furniture.position
                ax.add_patch(plt.Rectangle((y, x), furniture.width, furniture.height,
                                           color='gray', alpha=0.7))
                ax.text(y + furniture.width / 2, x + furniture.height / 2, furniture.name,
                        color='white', ha='center', va='center', fontsize=8)

        # Paramètres des axes
        ax.set_xlim(0, self.room.width)
        ax.set_ylim(0, self.room.height)
        ax.invert_yaxis()
        ax.set_title(f"Disposition de la pièce : {self.room.name}")
        ax.set_xlabel("Largeur (mètres)")
        ax.set_ylabel("Hauteur (mètres)")

        # Légende
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right')

        # Sauvegarder la figure
        filename = f"{self.room.name.replace(' ', '_')}_layout.png"
        filepath = os.path.join(self.SAVE_DIR, filename)
        fig.savefig(filepath)
        print(f"Graphique sauvegardé dans {filepath}")

        # Afficher
        plt.show()
