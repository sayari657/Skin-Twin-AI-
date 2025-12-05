"""
Tests pour le Model Registry
"""
import pytest
from mlops.deployment.model_registry import ModelRegistry


def test_model_registry_initialization():
    """Test l'initialisation du registry"""
    registry = ModelRegistry()
    assert registry is not None
    assert registry.tracking_uri is not None


def test_list_models():
    """Test la liste des modèles"""
    registry = ModelRegistry()
    models = registry.list_all_models()
    assert isinstance(models, list)

