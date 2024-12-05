import torch
import torch.nn as nn
import torch.nn.functional as F

class PlacementNet(nn.Module):
    def __init__(self, grid_size):
        super(PlacementNet, self).__init__()
        self.grid_size = grid_size
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * grid_size * grid_size, 128)
        self.fc2 = nn.Linear(128, grid_size * grid_size)  # Sortie : score pour chaque case de la grille

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x