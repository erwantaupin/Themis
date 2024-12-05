import matplotlib.pyplot as plt
import numpy as np

class Visualizer:
    def __init__(self, room, placements):
        self.room = room
        self.placements = placements

    def display_room(self):
        """Affiche la pièce avec les meubles placés et leurs noms."""
        grid = np.copy(self.room.grid)

        # Ajouter les meubles à la grille
        for furniture, x, y in self.placements:
            for i in range(furniture.height):
                for j in range(furniture.width):
                    grid[x + i, y + j] = 2  # Meubles en gris clair

        # Ajouter une couleur spéciale pour la porte
        if self.room.door:
            grid[self.room.door['x'], self.room.door['y']] = -2  # Code spécial pour la porte

        # Afficher la grille
        fig, ax = plt.subplots(figsize=(8, 8))
        cmap = plt.cm.get_cmap("Greys", 3)  # Gris avec 3 niveaux (fond, meubles, porte)
        cmap.set_under("blue")  # Colorier la porte en bleu

        # Affichage de la grille
        ax.imshow(grid, cmap=cmap, origin="upper", vmin=-2, vmax=2)

        # Ajouter les noms des meubles
        for furniture, x, y in self.placements:
            ax.text(
                y + furniture.width / 2,  # Centre du meuble
                x + furniture.height / 2,
                furniture.name,
                color="black",
                ha="center",
                va="center",
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white", alpha=0.8)
            )

        # Configuration des axes
        ax.set_xticks(range(self.room.width))
        ax.set_yticks(range(self.room.height))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(color="black", linestyle="--", linewidth=0.5)
        ax.set_title(f"Room Layout: {self.room.name}", fontsize=16)

        plt.colorbar(ax.imshow(grid, cmap=cmap, vmin=-2, vmax=2), ax=ax, ticks=[0, 1, 2])
        plt.show()