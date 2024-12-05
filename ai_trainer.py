import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
from model import PlacementNet

class PlacementAI:
    def __init__(self, room, wallet, grid_size=10):
        self.room = room
        self.wallet = wallet
        self.grid_size = grid_size
        self.model = PlacementNet(grid_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.CrossEntropyLoss()

    def generate_training_data(self):
        """Génère un dataset artificiel pour l'entraînement."""
        inputs = []
        targets = []

        for furniture in self.wallet:
            # Créer des états initiaux de la pièce
            grid = np.zeros((self.grid_size, self.grid_size))
            if self.room.door:
                grid[self.room.door['x'], self.room.door['y']] = -1  # Marquer la porte

            # Générer une cible aléatoire valide
            x = np.random.randint(0, self.grid_size - furniture.height)
            y = np.random.randint(0, self.grid_size - furniture.width)
            grid[x:x + furniture.height, y:y + furniture.width] = 1  # Meuble placé

            # Ajouter l'état et la cible
            inputs.append(grid)
            targets.append(x * self.grid_size + y)  # Index linéaire de la position

        # Convertir en un tableau NumPy avant de transformer en tenseur
        inputs = np.array(inputs)
        targets = np.array(targets)

        return torch.tensor(inputs, dtype=torch.float32).unsqueeze(1), torch.tensor(targets, dtype=torch.long)

    def train(self, epochs=100, batch_size=10):
        """Entraîne le réseau sur des exemples artificiels."""
        for epoch in range(epochs):
            inputs, targets = self.generate_training_data()
            dataset_size = inputs.size(0)

            for i in range(0, dataset_size, batch_size):
                batch_inputs = inputs[i:i + batch_size]
                batch_targets = targets[i:i + batch_size]

                # Forward
                self.optimizer.zero_grad()
                outputs = self.model(batch_inputs)
                loss = self.criterion(outputs, batch_targets)

                # Backward
                loss.backward()
                self.optimizer.step()

            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}")

        # Récupérer les meilleurs placements pour chaque meuble
        best_placements = []
        for furniture in self.wallet:
            grid = np.copy(self.room.grid)
            best_position = self.predict(grid)
            x, y = divmod(best_position, self.grid_size)
            best_placements.append((furniture, x, y))

        return best_placements

    def predict(self, grid):
        """Prédit les meilleures positions pour un meuble donné."""
        self.model.eval()
        with torch.no_grad():
            grid_tensor = torch.tensor(grid, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
            outputs = self.model(grid_tensor)
            return outputs.argmax().item()