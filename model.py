import torch
import torch.nn as nn
import torch.nn.functional as F

class PlacementNet(nn.Module):
    def __init__(self, height, width):
        super(PlacementNet, self).__init__()
        self.height = height
        self.width = width

        # Convolutions pour extraire des features spatiales
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)

        # Taille aplatir = 32 × height × width
        self.flatten_size = 32 * height * width

        # Réseaux fully‑connected
        self.fc1 = nn.Linear(self.flatten_size, 128)
        self.fc2 = nn.Linear(128, height * width)  # une sortie par case

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(x.size(0), -1)           # (batch, 32*H*W)
        x = F.relu(self.fc1(x))             # (batch, 128)
        x = self.fc2(x)                     # (batch, H*W)
        return x
