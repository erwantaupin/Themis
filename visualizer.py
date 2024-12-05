import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Visualizer:
    def __init__(self, room, placements):
        self.room = room
        self.placements = placements

    def display_room(self):
        """Affiche la pièce avec les meubles placés, les noms des meubles et la porte en bleu."""
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.room.width)
        ax.set_ylim(0, self.room.height)
        ax.set_aspect('equal')
        ax.set_xticks(range(self.room.width + 1))
        ax.set_yticks(range(self.room.height + 1))
        ax.grid(True)

        # Colorier la zone de la porte en bleu
        if self.room.door:
            door_x, door_y = self.room.door['x'], self.room.door['y']
            door_rect = patches.Rectangle((door_y, self.room.height - door_x - 1), 1, 1, linewidth=1, edgecolor='blue', facecolor='blue', alpha=0.5)
            ax.add_patch(door_rect)

        # Placer les meubles
        for furniture, x, y in self.placements:
            # Créer un rectangle pour le meuble
            rect = patches.Rectangle((y, self.room.height - x - furniture.height), furniture.width, furniture.height, linewidth=1, edgecolor='black', facecolor=furniture.color, alpha=0.7)
            ax.add_patch(rect)
            # Ajouter le nom du meuble centré
            cx = y + furniture.width / 2
            cy = self.room.height - (x + furniture.height / 2)
            ax.text(cx, cy, furniture.name, ha='center', va='center', fontsize=8, color='white')

        ax.set_title(f"Disposition des meubles dans la {self.room.name}")
        plt.gca().invert_yaxis()
        plt.show()