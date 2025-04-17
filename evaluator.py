import numpy as np

class Evaluator:
    def __init__(self, room, furniture_list):
        self.room = room
        self.furniture_list = furniture_list

    def evaluate(self):
        """Évalue la disposition complète en combinant les scores de chaque règle."""
        for furniture in self.furniture_list:
            if furniture.position is None:
                if furniture.type == 'tapis':
                    print(f"Finding position for rug '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_rug(furniture)
                elif furniture.type == 'meuble TV':
                    print(f"Finding position for TV '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_tv(furniture)
                elif furniture.type == 'coffre de rangement':
                    print("Current furniture positions:")
                    for furniture in self.furniture_list:
                        print(f"  {furniture.name} ({furniture.type}) -> Position: {furniture.position}")
                elif furniture.type == 'chaise de bureau':
                    print(f"Finding position for office chair '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_office_chair(furniture)
                elif furniture.type == 'armoire':
                    print(f"Finding position for armoire '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_armoire(furniture)
                elif furniture.type == 'buffet':
                    print(f"Finding position for buffet '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_buffet(furniture)
                elif furniture.type == 'évier':
                    print(f"Finding position for sink '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_sink(furniture)
                elif furniture.type == 'bureau' and furniture.position is None:
                    print(f"Finding position for desk '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_desk(furniture)
                elif furniture.type == 'panier à linge':
                    print(f"Finding position for laundry basket '{furniture.name}'.")
                    try:
                        furniture.position = self.find_best_position_for_laundry_basket(furniture)
                    except ValueError as e:
                        print(f"Error placing laundry basket: {e}. Assigning default position (0, 0).")
                        furniture.position = (0, 0)  # Position par défaut
                elif furniture.type == 'chaise':
                    print(f"Finding position for chair '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_chair(furniture)
                elif furniture.type == 'commode':
                    print(f"Finding position for dresser '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_dresser(furniture)
                elif furniture.type == 'toilettes':
                    print(f"Finding position for toilets '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_toilets(furniture)
                elif furniture.type == 'télévision':
                    print(f"Finding position for television '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_television(furniture)
                elif furniture.type == 'plante en pot':
                    print(f"Finding position for potted plant '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_potted_plant(furniture)
                elif furniture.type == 'four':
                    print(f"Finding position for oven '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_oven(furniture)
                elif furniture.type == 'lave-vaisselle':
                    print(f"Finding position for dishwasher '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_dishwasher(furniture)
                elif furniture.type == 'machine à laver':
                    print(f"Finding position for washing machine '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_machine(furniture)
                elif furniture.type == 'plaque chauffante':
                    print("Current furniture positions and dimensions:")
                    for furniture in self.furniture_list:
                        print(f"  {furniture.name} ({furniture.type}) -> Position: {furniture.position}, Dimensions: {furniture.width}x{furniture.height}")
                elif furniture.type == 'frigo':
                    print(f"Finding position for fridge '{furniture.name}'.")
                    furniture.position = self.find_best_position_for_fridge(furniture)
                else:
                    raise ValueError(f"Furniture '{furniture.name}' has no position set.")
        
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
            if furniture.position is None:
                print(f"Skipping obstruction check for {furniture.name}: no position set.")
                continue
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
            if furniture.type == 'chaise':
                if not self.is_near_table(furniture):
                    score -= 5  # Malus pour chaise non près d'une table
            if furniture.type == 'chaise de bureau':
                if not self.is_facing_desk(furniture):
                    score -= 10  # Malus si la chaise n'est pas face au bureau
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
        if furniture.position is None:
            return False  # Le meuble n'est pas encore placé
        x, y = furniture.position
        return x == 0 or y == 0 or x + furniture.height == self.room.height or y + furniture.width == self.room.width

    def is_obstructing_door(self, furniture):
        """Vérifie si un meuble obstrue une porte."""
        if furniture.position is None:
            return False  # Si le meuble n'a pas été placé, il ne peut pas obstruer une porte

        fx, fy = furniture.position
        fw, fh = furniture.width, furniture.height

        for door in self.room.doors:
            door_x, door_y = door['x'], door['y']
            if not (fx + fw <= door_x or fx >= door_x + 1 or fy + fh <= door_y or fy >= door_y + 1):
                return True  # Le meuble obstrue cette porte
        return False

    def is_obstructing_window(self, furniture):
        """Vérifie si un meuble obstrue une fenêtre."""
        if furniture.position is None:
            return False  # Si pas de position, le meuble ne peut pas obstruer
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
        pass  # Implémenter l'algorithme

    def is_symmetrical(self):
        """Vérifie si l'aménagement est symétrique."""
        pass  # Implémenter l'algorithme

    def has_focal_point(self):
        """Vérifie s'il existe un point focal dans la pièce."""
        pass  # Implémenter l'algorithme

    def has_adequate_spacing(self):
        """Vérifie si l'espacement entre les meubles est suffisant."""
        pass  # Implémenter l'algorithme

    def has_trip_hazards(self):
        """Vérifie s'il y a des risques de trébuchement."""
        pass  # Implémenter l'algorithme

    def is_layout_flexible(self):
        """Vérifie si l'aménagement est flexible."""
        pass  # Implémenter l'algorithme

    def is_overlapping(self, furniture, feature):
        """Vérifie si un meuble chevauche une porte ou une fenêtre."""
        if furniture.position is None:
            return False  # Si pas de position, pas de chevauchement

        fx, fy = furniture.position
        fw, fh = furniture.width, furniture.height
        ox, oy = feature['x'], feature['y']  # Extraire les coordonnées du dictionnaire

        return not (fx + fw <= ox or fx >= ox + 1 or fy + fh <= oy or fy >= oy + 1)

    def is_adjacent(self, furniture1, furniture2):
        """Vérifie si deux meubles sont adjacents."""
        fx, fy = furniture1.position
        fw, fh = furniture1.width, furniture1.height
        ox, oy = furniture2.position
        ow, oh = furniture2.width, furniture2.height
        return abs(fx - ox) <= 1 and abs(fy - oy) <= 1
    
    def find_best_position_for_rug(self, rug):
        """Trouve la meilleure position pour le tapis."""
        # Priorité : Devant le canapé
        for furniture in self.furniture_list:
            if furniture.type == 'canapé':
                return (furniture.position[0] + furniture.height, furniture.position[1])  # Juste devant

        # Ensuite : Sous le lit ou le bureau
        for furniture in self.furniture_list:
            if furniture.type in ['lit', 'bureau']:
                return furniture.position  # Même position que le meuble

        # Enfin : Trouver un espace libre
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, rug.width, rug.height):
                    return (x, y)

        # Si aucune position n'est trouvée, lever une erreur
        raise ValueError(f"No valid position found for rug '{rug.name}'.")
    
    def find_best_position_for_chest(self, chest):
        """Trouve la meilleure position pour le coffre de rangement."""
        print(f"Trying to place chest '{chest.name}'.")

        # Priorité : À côté de meubles spécifiques
        for furniture in self.furniture_list:
            if furniture.type in ['meuble TV', 'canapé', 'lit', 'bureau']:
                fx, fy = furniture.position
                if fx is not None and fy is not None:
                    # Vérifier les positions adjacentes autour du meuble
                    possible_positions = [
                        (fx - 1, fy),  # Au-dessus
                        (fx + furniture.height, fy),  # En-dessous
                        (fx, fy - 1),  # À gauche
                        (fx, fy + furniture.width)  # À droite
                    ]
                    for px, py in possible_positions:
                        if not self.is_space_occupied(px, py, chest.width, chest.height):
                            print(f"Placing chest '{chest.name}' next to '{furniture.name}' at ({px}, {py}).")
                            return (px, py)
                        else:
                            print(f"Position ({px}, {py}) near '{furniture.name}' is occupied.")

        # Ensuite : Contre un mur
        for x in range(self.room.height):
            for y in range(self.room.width):
                if x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1:  # Contre un mur
                    if not self.is_space_occupied(x, y, chest.width, chest.height):
                        print(f"Placing chest '{chest.name}' against a wall at ({x}, {y}).")
                        return (x, y)
                    else:
                        print(f"Wall position ({x}, {y}) is occupied.")

        # Enfin : Trouver un espace libre
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, chest.width, chest.height):
                    print(f"Placing chest '{chest.name}' in an open space at ({x}, {y}).")
                    return (x, y)
                else:
                    print(f"Open space position ({x}, {y}) is occupied.")

        # Si aucune position n'est trouvée, lever une erreur descriptive
        raise ValueError(f"No valid position found for chest '{chest.name}'.")
    
    def find_best_position_for_toilets(self, toilets):
        """Trouve la meilleure position pour les toilettes."""
        print(f"Trying to place toilets '{toilets.name}'.")

        # Priorité : Proche d'un mur et éloigné des zones de passage
        for x in range(self.room.width):
            for y in range(self.room.height):
                if (x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1):  # Contre un mur
                    if not self.is_space_occupied(x, y, toilets.width, toilets.height):
                        print(f"Placing toilets '{toilets.name}' against a wall at ({x}, {y}).")
                        return (x, y)

        # Ensuite : Trouver un espace libre éloigné des portes
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, toilets.width, toilets.height):
                    print(f"Placing toilets '{toilets.name}' in an open space at ({x}, {y}).")
                    return (x, y)

        # Si aucune position n'est trouvée, lever une erreur descriptive
        raise ValueError(f"No valid position found for toilets '{toilets.name}'.")
    
    def find_best_position_for_oven(self, oven):
        """Trouve la meilleure position pour le four."""
        # Priorité : À côté de l'évier ou du réfrigérateur
        for furniture in self.furniture_list:
            if furniture.type in ['évier', 'réfrigérateur']:
                fx, fy = furniture.position
                if fx is not None and fy is not None:
                    # Vérifier les positions adjacentes autour de l'évier ou du réfrigérateur
                    possible_positions = [
                       (fx - 1, fy),  # Au-dessus
                        (fx + furniture.height, fy),  # En-dessous
                        (fx, fy - 1),  # À gauche
                        (fx, fy + furniture.width)  # À droite
                    ]
                    for px, py in possible_positions:
                        if not self.is_space_occupied(px, py, oven.width, oven.height):
                            return (px, py)

        # Ensuite : Contre un mur dans la cuisine
        for x in range(self.room.height):
            for y in range(self.room.width):
                if x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1:  # Contre un mur
                   if not self.is_space_occupied(x, y, oven.width, oven.height):
                        return (x, y)

        # Si aucune position n'est trouvée, lever une erreur
        raise ValueError(f"No valid position found for oven '{oven.name}'.")

    def is_space_occupied(self, x, y, width, height):
        """Vérifie si une zone donnée est libre."""
        for furniture in self.furniture_list:
            if furniture.position is None:
                continue
            fx, fy = furniture.position
            fw, fh = furniture.width, furniture.height
            if not (x + width <= fx or x >= fx + fw or y + height <= fy or y >= fy + fh):
                print(f"Space ({x}, {y}, {width}, {height}) is occupied by {furniture.name} at ({fx}, {fy}, {fw}, {fh})")
                return True  # La zone est occupée
        return False
    
    def find_best_position_for_tv(self, tv):
        """Trouve la meilleure position pour le meuble TV."""
        # Priorité : Face au canapé
        for furniture in self.furniture_list:
            if furniture.type == 'canapé':
                # Positionner le TV face au canapé
                return (furniture.position[0], furniture.position[1] + furniture.width)

        # Ensuite : Face à la table basse
        for furniture in self.furniture_list:
            if furniture.type == 'table basse':
                # Positionner le TV face à la table basse
                return (furniture.position[0], furniture.position[1] + furniture.width)

        # Ensuite : Face à une table
        for furniture in self.furniture_list:
            if furniture.type == 'table':
                # Positionner le TV face à la table
                return (furniture.position[0], furniture.position[1] + furniture.width)

        # Enfin : Face à un fauteuil
        for furniture in self.furniture_list:
            if furniture.type == 'fauteuil':
                # Positionner le TV face au fauteuil
                return (furniture.position[0], furniture.position[1] + furniture.width)

        # Si aucune position n'est trouvée, lever une erreur
        raise ValueError(f"No valid position found for TV '{tv.name}'.")
    
    def find_best_position_for_buffet(self, buffet):
        """Trouve la meilleure position pour le buffet."""
        # Priorité : Contre un mur dans la salle à manger
        for x in range(self.room.width):
            for y in range(self.room.height):
                if (x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1):  # Contre un mur
                    if not self.is_space_occupied(x, y, buffet.width, buffet.height):
                        return (x, y)

        # Si aucune position n'est trouvée, placer dans un espace libre
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, buffet.width, buffet.height):
                    return (x, y)

        # Si aucune position n'est trouvée, lever une erreur
        raise ValueError(f"No valid position found for buffet '{buffet.name}'.")

    def find_best_position_for_sink(self, sink):
        """Trouve la meilleure position pour l'évier."""
        # Priorité : Contre un mur et sous une fenêtre
        for window in self.room.windows:
            wx, wy = window['x'], window['y']
            if not self.is_space_occupied(wx, wy - 1, sink.width, sink.height):
                return (wx, wy - 1)  # Juste sous la fenêtre

        # Ensuite : Contre un mur dans la cuisine
        for x in range(self.room.width):
            for y in range(self.room.height):
                if (x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1):  # Contre un mur
                    if not self.is_space_occupied(x, y, sink.width, sink.height):
                        return (x, y)

        # Si aucune position n'est trouvée, lever une erreur
        raise ValueError(f"No valid position found for sink '{sink.name}'.")
    
    def is_facing_desk(self, chair):
        """Vérifie si la chaise de bureau est correctement positionnée face au bureau."""
        for furniture in self.furniture_list:
            if furniture.type == 'bureau':  # Identifier le bureau
                # Vérifier si la chaise est alignée avec le bureau
                cx, cy = chair.position
                bx, by = furniture.position
                bw, bh = furniture.width, furniture.height
                # La chaise est considérée "face au bureau" si elle est alignée devant
                if bx <= cx < bx + bw and cy == by - 1:  # Devant le bureau
                    return True
        return False
    
    def find_best_position_for_office_chair(self, chair):
        """Trouve la meilleure position pour la chaise de bureau."""
        # Vérifiez s'il existe un bureau dans la pièce
        for furniture in self.furniture_list:
            if furniture.type == 'bureau':
                bx, by = furniture.position
                if bx is not None and by is not None:  # Vérifiez que le bureau a une position définie
                    # Essayez de placer la chaise devant le bureau
                    if not self.is_space_occupied(bx, by - 1, chair.width, chair.height):
                        return (bx, by - 1)  # Position devant le bureau

        # Si aucun bureau ou si la position est occupée, placez dans un espace libre
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, chair.width, chair.height):
                    return (x, y)  # Première position libre trouvée

        # Si aucune position n'est trouvée, retourner une position par défaut
        print(f"No valid position found for office chair '{chair.name}', placing at default position (0, 0).")
        return (0, 0)
    
    def find_best_position_for_armoire(self, armoire):
        """Trouve la meilleure position pour l'armoire."""
        # Priorité : Contre un mur et proche du lit
        for furniture in self.furniture_list:
            if furniture.type == 'lit':  # Identifier le lit
                lx, ly = furniture.position
                # Chercher une position contre un mur proche du lit
                if lx > 0:  # Mur en haut du lit
                    return (lx - 1, ly)
                if lx + furniture.height < self.room.height:  # Mur en bas du lit
                    return (lx + furniture.height, ly)
                if ly > 0:  # Mur à gauche du lit
                    return (lx, ly - 1)
                if ly + furniture.width < self.room.width:  # Mur à droite du lit
                    return (lx, ly + furniture.width)

        # Si aucun lit n'est présent, placer contre n'importe quel mur
        for x in range(self.room.height):
            for y in range(self.room.width):
                if x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1:  # Contre un mur
                    if not self.is_space_occupied(x, y, armoire.width, armoire.height):
                        return (x, y)

        # Si aucune position n'est trouvée, lever une erreur
        raise ValueError(f"No valid position found for armoire '{armoire.name}'.")
    
    def find_best_position_for_chair(self, chair):
        """Trouve la meilleure position pour une chaise."""
        for furniture in self.furniture_list:
            if furniture.type in ['table', 'bureau']:
                tx, ty = furniture.position
                if not self.is_space_occupied(tx, ty - 1, chair.width, chair.height):  # À côté de la table ou bureau
                    return (tx, ty - 1)

        # Si aucune table ou bureau, placez dans un espace libre
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, chair.width, chair.height):
                    return (x, y)

        raise ValueError(f"No valid position found for chair '{chair.name}'.")
    
    def find_best_position_for_potted_plant(self, plant):
        """Trouve la meilleure position pour une plante en pot."""
        # Priorité : Proche d'une fenêtre
        for window in self.room.windows:
            wx, wy = window['x'], window['y']
            possible_positions = [
                (wx - 1, wy),  # Au-dessus
                (wx + 1, wy),  # En-dessous
                (wx, wy - 1),  # À gauche
                (wx, wy + 1)   # À droite
            ]
            for px, py in possible_positions:
                if not self.is_space_occupied(px, py, plant.width, plant.height):
                    return (px, py)

        # Ensuite : Dans un coin de la pièce
        corners = [
            (0, 0),  # Coin haut-gauche
            (self.room.height - 1, 0),  # Coin bas-gauche
            (0, self.room.width - 1),  # Coin haut-droit
            (self.room.height - 1, self.room.width - 1)  # Coin bas-droit
        ]
        for cx, cy in corners:
            if not self.is_space_occupied(cx, cy, plant.width, plant.height):
                return (cx, cy)

        # Enfin : Trouver un espace libre quelconque
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, plant.width, plant.height):
                    return (x, y)

        # Si aucune position n'est trouvée, lever une erreur
        raise ValueError(f"No valid position found for potted plant '{plant.name}'.")
    
    def find_best_position_for_dresser(self, dresser):
        """Trouve la meilleure position pour une commode."""
        for x in range(self.room.width):
            for y in range(self.room.height):
                if (x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1):  # Contre un mur
                    if not self.is_space_occupied(x, y, dresser.width, dresser.height):
                        return (x, y)

        raise ValueError(f"No valid position found for dresser '{dresser.name}'.")
    
    def find_best_position_for_television(self, television):
        """Trouve la meilleure position pour une télévision."""
        # Priorité : Face au canapé ou au fauteuil
        for furniture in self.furniture_list:
            if furniture.type in ['canapé', 'fauteuil']:
                if furniture.position is None:
                    print(f"Warning: {furniture.name} ({furniture.type}) has no position set.")
                    continue

                cx, cy = furniture.position
                if not self.is_space_occupied(cx - 1, cy, television.width, television.height):
                    return (cx - 1, cy)

        # Ensuite : Contre un mur
        for x in range(self.room.height):
            for y in range(self.room.width):
                if x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1:
                    if not self.is_space_occupied(x, y, television.width, television.height):
                        return (x, y)

        # Enfin : Trouver un espace libre
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, television.width, television.height):
                    return (x, y)

        # Si aucune position n'est trouvée, lever une erreur
        raise ValueError(f"No valid position found for television '{television.name}'.")
    
    def find_best_position_for_laundry_basket(self, basket):
        """Trouve la meilleure position pour le panier à linge."""
        print(f"Trying to place laundry basket '{basket.name}'.")

        # Priorité : Proche du lit ou de la machine à laver et contre un mur
        for furniture in self.furniture_list:
            if furniture.type in ['lit', 'machine à laver']:
                fx, fy = furniture.position
                if fx is not None and fy is not None:
                    # Chercher une position contre un mur proche de l'objet
                    possible_positions = [
                        (fx - 1, fy),  # Mur au-dessus
                        (fx + furniture.height, fy),  # Mur en dessous
                        (fx, fy - 1),  # Mur à gauche
                        (fx, fy + furniture.width)  # Mur à droite
                    ]
                    for px, py in possible_positions:
                        if not self.is_space_occupied(px, py, basket.width, basket.height):
                            print(f"Placing laundry basket '{basket.name}' next to '{furniture.name}' at ({px}, {py}).")
                            return (px, py)
                        else:
                            print(f"Position ({px}, {py}) near '{furniture.name}' is occupied.")

        # Ensuite : Placer contre un mur quelconque
        for x in range(self.room.height):
            for y in range(self.room.width):
                if x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1:  # Contre un mur
                    if not self.is_space_occupied(x, y, basket.width, basket.height):
                        print(f"Placing laundry basket '{basket.name}' against a wall at ({x}, {y}).")
                        return (x, y)

        # Enfin : Position par défaut si aucune position n'est trouvée
        print(f"No valid position found for laundry basket '{basket.name}', assigning default position (0, 0).")
        return (0, 0)
    
    def find_best_position_for_machine(self, machine):
        """Trouve la meilleure position pour la machine à laver."""
        print(f"Trying to place washing machine '{machine.name}'.")

        # Priorité : Proche de l'évier
        for furniture in self.furniture_list:
            if furniture.type == 'évier' and furniture.position is not None:
                fx, fy = furniture.position
                possible_positions = [
                    (fx - 1, fy),  # Au-dessus
                    (fx + 1, fy),  # En-dessous
                    (fx, fy - 1),  # À gauche
                    (fx, fy + 1)   # À droite
                ]
                for px, py in possible_positions:
                    if not self.is_space_occupied(px, py, machine.width, machine.height):
                        print(f"Placing washing machine '{machine.name}' next to sink at ({px}, {py}).")
                        return (px, py)
                    else:
                        print(f"Position ({px}, {py}) near sink is occupied.")

        # Ensuite : Contre un mur dans la buanderie
        for x in range(self.room.height):
            for y in range(self.room.width):
                if x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1:  # Contre un mur
                    if not self.is_space_occupied(x, y, machine.width, machine.height):
                        print(f"Placing washing machine '{machine.name}' against a wall at ({x}, {y}).")
                        return (x, y)

        # Enfin : Trouver un espace libre
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, machine.width, machine.height):
                    print(f"Placing washing machine '{machine.name}' in open space at ({x}, {y}).")
                    return (x, y)
                else:
                    print(f"Open space position ({x}, {y}) is occupied.")

        # Si aucune position n'est trouvée, lever une erreur descriptive
        raise ValueError(f"No valid position found for washing machine '{machine.name}'.")
        
    def find_best_position_for_dishwasher(self, dishwasher):
        """Trouve la meilleure position pour le lave-vaisselle."""
        # Priorité : Proche de l'évier
        for furniture in self.furniture_list:
            if furniture.type == 'évier' and furniture.position is not None:
                fx, fy = furniture.position
                possible_positions = [
                    (fx - 1, fy),  # Au-dessus
                    (fx + 1, fy),  # En-dessous
                    (fx, fy - 1),  # À gauche
                    (fx, fy + 1)   # À droite
                ]
                for px, py in possible_positions:
                    if not self.is_space_occupied(px, py, dishwasher.width, dishwasher.height):
                        return (px, py)

        # Ensuite : Contre un mur dans la cuisine
        for x in range(self.room.height):
            for y in range(self.room.width):
                if (x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1):  # Contre un mur
                    if not self.is_space_occupied(x, y, dishwasher.width, dishwasher.height):
                        return (x, y)

        # Enfin : Trouver un espace libre
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, dishwasher.width, dishwasher.height):
                    return (x, y)

        # Si aucune position n'est trouvée, lever une erreur
        raise ValueError(f"No valid position found for dishwasher '{dishwasher.name}'.")
    
    def find_best_position_for_fridge(self, fridge):
        """Trouve la meilleure position pour le réfrigérateur."""
        # Priorité : Contre un mur
        for x in range(self.room.height):
            for y in range(self.room.width):
                if x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1:  # Contre un mur
                    if not self.is_space_occupied(x, y, fridge.width, fridge.height):
                        return (x, y)

        # Ensuite : Proche de l'évier ou d'autres meubles de cuisine
        for furniture in self.furniture_list:
            if furniture.type in ['évier', 'plan de travail']:
                fx, fy = furniture.position
                if fx is not None and fy is not None:
                    possible_positions = [
                        (fx - 1, fy),  # Au-dessus
                        (fx + 1, fy),  # En-dessous
                        (fx, fy - 1),  # À gauche
                        (fx, fy + 1)   # À droite
                    ]
                    for px, py in possible_positions:
                        if not self.is_space_occupied(px, py, fridge.width, fridge.height):
                            return (px, py)

        # Enfin : Trouver un espace libre
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, fridge.width, fridge.height):
                    return (x, y)

        # Si aucune position n'est trouvée, lever une erreur
        raise ValueError(f"No valid position found for fridge '{fridge.name}'.")
    
    def find_best_position_for_cooktop(self, cooktop):
        """Trouve la meilleure position pour la cuisinière."""
        print(f"Trying to place cooktop '{cooktop.name}'.")

        # Priorité : Proche du plan de travail ou de l'évier
        for furniture in self.furniture_list:
            if furniture.type in ['plan de travail', 'évier']:
                fx, fy = furniture.position
                if fx is not None and fy is not None:
                    possible_positions = [
                        (fx - 1, fy),  # Au-dessus
                        (fx + 1, fy),  # En-dessous
                        (fx, fy - 1),  # À gauche
                        (fx, fy + 1)   # À droite
                    ]
                    for px, py in possible_positions:
                        if not self.is_space_occupied(px, py, cooktop.width, cooktop.height):
                            print(f"Placing cooktop '{cooktop.name}' next to '{furniture.name}' at ({px}, {py}).")
                            return (px, py)
                        else:
                            print(f"Position ({px}, {py}) near '{furniture.name}' is occupied.")

        # Ensuite : Contre un mur dans la cuisine
        for x in range(self.room.height):
            for y in range(self.room.width):
                if x == 0 or y == 0 or x == self.room.height - 1 or y == self.room.width - 1:
                    if not self.is_space_occupied(x, y, cooktop.width, cooktop.height):
                        print(f"Placing cooktop '{cooktop.name}' against a wall at ({x}, {y}).")
                        return (x, y)
                    else:
                        print(f"Wall position ({x}, {y}) is occupied.")

        # Enfin : Trouver un espace libre
        for x in range(self.room.width):
            for y in range(self.room.height):
                if not self.is_space_occupied(x, y, cooktop.width, cooktop.height):
                    print(f"Placing cooktop '{cooktop.name}' in open space at ({x}, {y}).")
                    return (x, y)
                else:
                    print(f"Open space position ({x}, {y}) is occupied.")

        # Si aucune position n'est trouvée, lever une erreur descriptive
        raise ValueError(f"No valid position found for cooktop '{cooktop.name}'.")