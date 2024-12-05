import random
from placement_logic import PlacementLogic
from evaluator import Evaluator  # Ajout de l'import

class PlacementAI:
    def __init__(self, room, wallet):
        self.room = room
        self.wallet = wallet
        self.evaluator = Evaluator(room, wallet)  # Initialisation de l'évaluateur

    def train(self, iterations=100):
        best_score = float('-inf')
        best_placements = []

        for _ in range(iterations):
            current_score = 0
            placements = []

            self.room.reset_grid()

            for furniture in self.wallet:
                attempts = 10
                best_position = None
                best_local_score = float('-inf')

                for _ in range(attempts):
                    x = random.randint(0, self.room.height - furniture.height)
                    y = random.randint(0, self.room.width - furniture.width)
                    if self.room.can_place_furniture(x, y, furniture):
                        local_score = PlacementLogic.calculate_score(self.room, x, y, furniture, placements)
                        if local_score > best_local_score:
                            best_local_score = local_score
                            best_position = (x, y)

                if best_position:
                    x, y = best_position
                    self.room.place_furniture(x, y, furniture)
                    placements.append((furniture, x, y))
                    current_score += best_local_score

            # Utilisation de l'évaluation pour ajuster le score
            evaluator_score = self.evaluator.evaluate()
            current_score += evaluator_score

            if current_score > best_score:
                best_score = current_score
                best_placements = placements

        print(f"Meilleur score final : {best_score}")
        return best_placements