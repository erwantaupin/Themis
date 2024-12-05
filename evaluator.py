import numpy as np

class Evaluator:
    def __init__(self, room, furniture_list):
        self.room = room
        self.furniture_list = furniture_list

    def evaluate(self):
        """Évalue la disposition complète en combinant les scores de chaque règle."""
        score = 0
        score += self.evaluate_wall_placement()
        score += self.evaluate_obstruction()
        score += self.evaluate_functional_grouping()
        score += self.evaluate_specific_rules()
        score += self.evaluate_circulation()
        score += self.evaluate_aesthetics()
        score += self.evaluate_comfort()
        score += self.evaluate_safety()
        score += self.evaluate_flexibility()
        return score

    def evaluate_wall_placement(self):
        """Évalue si les meubles appropriés sont placés contre les murs."""
        score = 0
        for furniture in self.furniture_list:
            if furniture.type in ['armoire', 'lit', 'canapé'] and not self.is_against_wall(furniture):
                score -= 10  # Malus si ces meubles ne sont pas contre un mur
        return score

    def evaluate_obstruction(self):
        """Vérifie si des meubles obstruent les portes ou les fenêtres."""
        score = 0
        for furniture in self.furniture_list:
            if self.is_obstructing_door(furniture):
                score -= 15  # Malus pour obstruction de porte
            if self.is_obstructing_window(furniture):
                score -= 5  # Malus pour obstruction de fenêtre
        return score

    def evaluate_functional_grouping(self):
        """Évalue le regroupement fonctionnel des meubles."""
        score = 0
        kitchen_items = ['réfrigérateur', 'cuisinière', 'évier']
        kitchen_positions = [furniture.position for furniture in self.furniture_list if furniture.type in kitchen_items]
        if self.are_items_grouped(kitchen_positions):
            score += 10  # Bonus si les éléments de cuisine sont regroupés
        return score

    def evaluate_specific_rules(self):
        """Applique des règles spécifiques pour certains meubles."""
        score = 0
        for furniture in self.furniture_list:
            if furniture.type == 'lit':
                if self.room.type == 'salon':
                    score -= 5  # Malus pour lit dans le salon
                if not self.is_against_wall(furniture):
                    score -= 10  # Malus pour lit non contre un mur
            if furniture.type == 'chaise' and not self.is_near_table(furniture):
                score -= 5  # Malus pour chaise non près d'une table
        return score

    def evaluate_circulation(self):
        """Vérifie si les passages sont dégagés."""
        score = 10 if self.has_clear_pathways() else -10
        return score

    def evaluate_aesthetics(self):
        """Évalue l'esthétique générale de l'aménagement."""
        score = 0
        if self.is_symmetrical():
            score += 5  # Bonus pour symétrie
        if self.has_focal_point():
            score += 5  # Bonus pour point focal
        return score

    def evaluate_comfort(self):
        """Évalue le confort de l'aménagement."""
        return 5 if self.has_adequate_spacing() else -5

    def evaluate_safety(self):
        """Vérifie s'il y a des risques de trébuchement."""
        return 5 if not self.has_trip_hazards() else -5

    def evaluate_flexibility(self):
        """Vérifie si l'aménagement est flexible."""
        return 5 if self.is_layout_flexible() else -5

    # Méthodes auxiliaires
    def is_against_wall(self, furniture):
        """Vérifie si un meuble est placé contre un mur."""
        x, y = furniture.position
        return x == 0 or y == 0 or x + furniture.height == self.room.height or y + furniture.width == self.room.width

    def is_obstructing_door(self, furniture):
        """Vérifie si un meuble obstrue une porte."""
        for door in self.room.doors:
            if self.is_overlapping(furniture, door):
                return True
        return False

    def is_obstructing_window(self, furniture):
        """Vérifie si un meuble obstrue une fenêtre."""
        for window in self.room.windows:
            if self.is_overlapping(furniture, window):
                return True
        return False

    def are_items_grouped(self, positions):
        """Vérifie si les éléments sont regroupés dans un certain rayon."""
        if not positions:
            return False
        centroid = np.mean(positions, axis=0)
        for pos in positions:
            if np.linalg.norm(np.array(pos) - centroid) > 2:  # Rayon de regroupement de 2 unités
                return False
        return True

    def is_near_table(self, furniture):
        """Vérifie si une chaise est près d'une table."""
        for other in self.furniture_list:
            if other.type == 'table' and self.is_adjacent(furniture, other):
                return True
        return False

    def has_clear_pathways(self):
        """Vérifie si les passages sont dégagés."""
        # Déterminer un chemin entre la porte et les zones clés
        # Exécutez un algorithme de recherche de chemin tel que BFS
        pass

    def is_symmetrical(self):
        """Vérifie si l'aménagement est symétrique."""
        # Calculez les distances des meubles par rapport au centre et vérifiez la symétrie
        pass

    def has_focal_point(self):
        """Vérifie s'il existe un point focal dans la pièce."""
        # Vérifiez si un meuble principal est visible depuis l'entrée
        pass

    def has_adequate_spacing(self):
        """Vérifie si l'espacement entre les meubles est suffisant."""
        # S'assurer qu'il y a au moins 60 cm entre chaque meuble
        pass

    def has_trip_hazards(self):
        """Vérifie s'il y a des risques de trébuchement."""
        # Vérifiez les obstacles tels que des tapis ou des meubles mal placés
        pass

    def is_layout_flexible(self):
        """Vérifie si l'aménagement est flexible."""
        # Vérifiez si les meubles peuvent être déplacés facilement pour réorganiser la pièce
        pass

    def is_overlapping(self, furniture, feature):
        """Vérifie si un meuble chevauche une porte ou une fenêtre."""
        fx, fy = furniture.position
        fw, fh = furniture.width, furniture.height
        ox, oy = feature.position
        ow, oh = feature.width, feature.height
        return not (fx + fw <= ox or fx >= ox + ow or fy + fh <= oy or fy >= oy + oh)

    def is_adjacent(self, furniture1, furniture2):
        """Vérifie si deux meubles sont adjacents."""
        fx, fy = furniture1.position
        fw, fh = furniture1.width, furniture1.height
        ox, oy = furniture2.position
        ow, oh = furniture2.width, furniture2.height
        return abs(fx - ox) <= 1 and abs(fy - oy) <= 1
