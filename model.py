"""Shared training and inference contract."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps
import torch
from torch import nn

ROOT = Path(__file__).resolve().parent
LETTERS = 'ABCDEFGHIKLMNOPQRSTUVWXY'

class SignCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(1, 24, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(24, 48, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Flatten(), nn.Linear(48*7*7, 128), nn.ReLU(),
            nn.Dropout(.25), nn.Linear(128, 24))
    def forward(self, x):
        return self.layers(x)

def preprocess(image):
    image = ImageOps.exif_transpose(image).convert('L').resize((28, 28), Image.Resampling.BILINEAR)
    array = np.asarray(image, dtype=np.float32).copy() / 255.
    return torch.from_numpy(array).reshape(1, 1, 28, 28), image

def load_model():
    model = SignCNN()
    model.load_state_dict(torch.load(ROOT/'artifacts/model.pt', map_location='cpu', weights_only=True))
    return model.eval()

def predict(model, image):
    tensor, processed = preprocess(image)
    with torch.inference_mode():
        values, indices = model(tensor).softmax(1)[0].topk(3)
    return [{'letter': LETTERS[i], 'probability': round(float(p), 6)} for p, i in zip(values, indices)], processed
