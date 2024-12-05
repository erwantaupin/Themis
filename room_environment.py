import gym
from evaluator import Evaluator

class RoomEnvironment(gym.Env):
    def __init__(self, room, furniture_list):
        self.room = room
        self.furniture_list = furniture_list
        self.evaluator = Evaluator(room, furniture_list)
        self.reset()

    def reset(self):
        self.room.reset_grid()
        return self._get_state()

    def step(self, action):
        # Appliquer une action : placer un meuble
        furniture, position = action
        x, y = position
        if self.room.can_place_furniture(x, y, furniture):
            self.room.place_furniture(x, y, furniture)
        
        # Évaluer le résultat après l'action
        reward = self.evaluator.evaluate()
        done = self._is_done()
        return self._get_state(), reward, done, {}

    def _get_state(self):
        # Retourne l'état actuel (par exemple, la grille et les positions des meubles)
        return self.room.grid.copy()

    def _is_done(self):
        # Terminer lorsque tous les meubles sont placés
        return all(furniture.placed for furniture in self.furniture_list)