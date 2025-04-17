class PlacementLogic:
    @staticmethod
    def calculate_score(room, x, y, furniture, placements):
        score = 0

        # Règle : bonus si une chaise est adjacente à une table
        if furniture.name == "Chaise":
            for other_furniture, ox, oy in placements:
                if other_furniture.name == "Table":
                    if abs(x - ox) <= 1 and abs(y - oy) <= 1:
                        score += 10

        # Règle : bonus si la télévision est en face d'un canapé
        if furniture.name == "Télévision":
            for other_furniture, ox, oy in placements:
                if other_furniture.name == "Canapé":
                    if x == ox and abs(y - oy) <= 3:
                        score += 15

        # Règle : malus si le meuble obstrue le chemin vers la porte
        if room.doors:
            for door in room.doors:
                door_x, door_y = door['x'], door['y']
                if x <= door_x < x + furniture.height and y <= door_y < y + furniture.width:
                    score -= 20

        # Règle : malus si le lit est trop près de la cuisine
        if furniture.name == "Lit":
            for other_furniture, ox, oy in placements:
                if other_furniture.name in ["Réfrigérateur", "Four", "Évier"]:
                    if abs(x - ox) <= 2 and abs(y - oy) <= 2:
                        score -= 10

        # Règle : bonus si le bureau est près d'une fenêtre
        if furniture.name == "Bureau" and room.has_window_near(x, y):
            score += 5

        return score