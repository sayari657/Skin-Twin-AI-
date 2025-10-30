"""
Modèle CNN pour la classification du type de peau
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models


class SkinTypeClassifier(nn.Module):
    """Classificateur de type de peau basé sur ResNet"""
    
    def __init__(self, num_classes=5, pretrained=True):
        super(SkinTypeClassifier, self).__init__()
        
        # Utiliser ResNet18 comme backbone
        self.backbone = models.resnet18(pretrained=pretrained)
        
        # Remplacer la dernière couche
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
        
    def forward(self, x):
        return self.backbone(x)


class EfficientNetSkinClassifier(nn.Module):
    """Classificateur utilisant EfficientNet"""
    
    def __init__(self, num_classes=5):
        super(EfficientNetSkinClassifier, self).__init__()
        
        # Utiliser EfficientNet-B0
        from torchvision.models import efficientnet_b0
        self.backbone = efficientnet_b0(pretrained=True)
        
        # Remplacer la dernière couche
        num_features = self.backbone.classifier[1].in_features
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )
        
    def forward(self, x):
        return self.backbone(x)


def create_skin_classifier(model_type='resnet', num_classes=5):
    """Créer un classificateur de type de peau"""
    
    if model_type == 'resnet':
        model = SkinTypeClassifier(num_classes=num_classes)
    elif model_type == 'efficientnet':
        model = EfficientNetSkinClassifier(num_classes=num_classes)
    else:
        raise ValueError(f"Type de modèle non supporté: {model_type}")
    
    return model


def load_pretrained_model(model_path, model_type='resnet', device='cpu'):
    """Charger un modèle pré-entraîné"""
    
    model = create_skin_classifier(model_type)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    
    return model


# Types de peau supportés
SKIN_TYPES = ['DRY', 'OILY', 'COMBINATION', 'NORMAL', 'SENSITIVE']
SKIN_TYPE_LABELS = {
    'DRY': 'Sèche',
    'OILY': 'Grasse', 
    'COMBINATION': 'Mixte',
    'NORMAL': 'Normale',
    'SENSITIVE': 'Sensible'
}




