import os
import torch
import torch.optim as optim
from model import PlacementNet
from evaluator import Evaluator

class PlacementAI:
    SAVE_DIR = "save"
    INITIAL_MODEL_PATH = os.path.join(SAVE_DIR, "initial_model.pth")
    FINAL_MODEL_PATH = os.path.join(SAVE_DIR, "final_model.pth")

    def __init__(self, room, wallet):
        self.room = room
        self.wallet = wallet
        self.evaluator = Evaluator(room, wallet)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Créer le dossier de sauvegarde s'il n'existe pas
        os.makedirs(self.SAVE_DIR, exist_ok=True)

        # Instancier le modèle
        height, width = room.height, room.width
        self.model = PlacementNet(height, width).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)

        # Charger le modèle final s'il existe, sinon sauvegarder l'initial
        if os.path.exists(self.FINAL_MODEL_PATH):
            self.model.load_state_dict(torch.load(self.FINAL_MODEL_PATH, map_location=self.device))
            print(f"Modèle chargé depuis {self.FINAL_MODEL_PATH}")
        else:
            torch.save(self.model.state_dict(), self.INITIAL_MODEL_PATH)
            print(f"Modèle initial sauvegardé dans {self.INITIAL_MODEL_PATH}")

        self.best_score = None
        self.current_score = None
        self.best_placements = []

    def train(self, episodes=100):
        all_rewards = []
        for episode in range(episodes):
            log_probs = []
            self.room.reset_grid()
            placements = []

            for furniture in self.wallet:
                grid = self.room.grid
                state = torch.tensor(grid, dtype=torch.float32, device=self.device).unsqueeze(0).unsqueeze(0)
                scores = self.model(state).view(-1)

                H, W = self.room.height, self.room.width
                mask = torch.zeros_like(scores)
                idx = 0
                for x in range(H):
                    for y in range(W):
                        if self.room.is_position_valid(x, y, furniture):
                            mask[idx] = 1
                        idx += 1

                scores_masked = scores.clone()
                scores_masked[mask == 0] = -1e9
                probs = torch.softmax(scores_masked, dim=0)

                m = torch.distributions.Categorical(probs)
                action_idx = m.sample()
                log_probs.append(m.log_prob(action_idx))

                x = action_idx.item() // W
                y = action_idx.item() % W
                self.room.place_furniture(x, y, furniture)
                placements.append((furniture, x, y))

            reward = self.evaluator.evaluate()
            all_rewards.append(reward)
            baseline = sum(all_rewards) / len(all_rewards)

            loss = sum(-lp * (reward - baseline) for lp in log_probs)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            self.current_score = reward
            if self.best_score is None or reward > self.best_score:
                self.best_score = reward
                self.best_placements = placements

            print(f"Episode {episode+1}/{episodes}, reward={reward}, best={self.best_score}")

        # Sauvegarder le modèle final
        torch.save(self.model.state_dict(), self.FINAL_MODEL_PATH)
        print(f"Modèle final sauvegardé dans {self.FINAL_MODEL_PATH}")
        return self.best_placements

    def predict(self):
        # Charger le modèle final
        if os.path.exists(self.FINAL_MODEL_PATH):
            self.model.load_state_dict(torch.load(self.FINAL_MODEL_PATH, map_location=self.device))
            print(f"Modèle pour test chargé depuis {self.FINAL_MODEL_PATH}")
        else:
            raise FileNotFoundError("Modèle final introuvable. Exécutez train() d'abord.")

        self.room.reset_grid()
        placements = []
        H, W = self.room.height, self.room.width
        for furniture in self.wallet:
            grid = self.room.grid
            state = torch.tensor(grid, dtype=torch.float32, device=self.device).unsqueeze(0).unsqueeze(0)
            scores = self.model(state).view(-1)

            mask = torch.zeros_like(scores)
            idx = 0
            for x in range(H):
                for y in range(W):
                    if self.room.is_position_valid(x, y, furniture):
                        mask[idx] = 1
                    idx += 1

            scores_masked = scores.clone()
            scores_masked[mask == 0] = -1e9

            action_idx = torch.argmax(scores_masked).item()
            x = action_idx // W
            y = action_idx % W
            self.room.place_furniture(x, y, furniture)
            placements.append((furniture, x, y))

        return placements
