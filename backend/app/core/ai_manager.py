"""
AI Manager - Singleton pour gestion des modèles IA
Charge les modèles au démarrage et les garde en mémoire
"""
from typing import Optional
import torch
from transformers import pipeline
from app.core.config import settings


class AIManager:
    """Singleton pour gérer les modèles IA"""
    
    _instance: Optional['AIManager'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.phishing_classifier = None
            self._initialized = True
    
    async def load_models(self):
        """Charge tous les modèles IA au démarrage"""
        print("🔄 Chargement des modèles IA...")
        
        try:
            # Déterminer le device (CPU/GPU)
            device = -1  # CPU par défaut
            if settings.AI_DEVICE == "cuda" and torch.cuda.is_available():
                device = 0
                print("🎮 GPU CUDA détecté - utilisation du GPU")
            elif settings.AI_DEVICE == "mps" and torch.backends.mps.is_available():
                device = 0
                print("🍎 Apple Silicon (MPS) détecté")
            else:
                print("💻 Utilisation du CPU pour l'inférence")
            
            # Charger le modèle de détection de phishing
            print(f"📦 Chargement du modèle: {settings.HF_PHISHING_MODEL}")
            self.phishing_classifier = pipeline(
                "text-classification",
                model=settings.HF_PHISHING_MODEL,
                device=device,
                truncation=True,
                max_length=512
            )
            
            print("✅ Modèles IA chargés avec succès")
            print(f"   - Phishing Detection: {settings.HF_PHISHING_MODEL}")
            print(f"   - Device: {'GPU' if device >= 0 else 'CPU'}")
            
        except Exception as e:
            print(f"⚠️  Erreur lors du chargement des modèles IA: {e}")
            print("   Le service fonctionnera en mode dégradé (heuristique)")
            self.phishing_classifier = None
    
    async def unload_models(self):
        """Décharge les modèles (appelé à l'arrêt)"""
        print("🔄 Déchargement des modèles IA...")
        
        if self.phishing_classifier:
            del self.phishing_classifier
            self.phishing_classifier = None
        
        # Force garbage collection
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        print("✅ Modèles IA déchargés")
    
    def get_phishing_classifier(self):
        """Retourne le classificateur de phishing"""
        return self.phishing_classifier
    
    def is_available(self) -> bool:
        """Vérifie si les modèles IA sont disponibles"""
        return self.phishing_classifier is not None


# Instance globale singleton
ai_manager = AIManager()


# Helper functions
async def load_ai_models():
    """Charge les modèles au démarrage de l'application"""
    await ai_manager.load_models()


async def unload_ai_models():
    """Décharge les modèles à l'arrêt de l'application"""
    await ai_manager.unload_models()


def get_ai_manager() -> AIManager:
    """Retourne l'instance du AI Manager"""
    return ai_manager



