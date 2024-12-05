class PlacementLogic:
    @staticmethod
    def calculate_score(room, x, y, furniture):
        """Calcule le score d'un placement donné."""
        score = 100  # Score de base

        # Règle 1 : Meuble devant une porte
        if room.door and x <= room.door['x'] < x + furniture.height and y <= room.door['y'] < y + furniture.width:
            score -= 50  # Malus important pour bloquer une porte

        # Règle 2 : Meuble non collé à un mur
        if x > 0 and x + furniture.height < room.height and \
           y > 0 and y + furniture.width < room.width:
            score -= 20  # Malus si le meuble n'est pas collé à un mur

        return score