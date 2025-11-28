"""
Configuration globale de l'application
Gestion des variables d'environnement et paramètres
"""
import os
from pydantic_settings import BaseSettings
from typing import List, Optional
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()


class Settings(BaseSettings):
    """Configuration de l'application via variables d'environnement"""
    
    # Application
    APP_NAME: str = "Cyber IA Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API
    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
    ]
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production-please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./cyber_ia.db"
    
    # ============================================
    # EXTERNAL APIs KEYS (from .env)
    # ============================================
    
    # AbuseIPDB API Key
    ABUSEIPDB_API_KEY: Optional[str] = None
    ABUSEIPDB_BASE_URL: str = "https://api.abuseipdb.com/api/v2"
    
    # VirusTotal API Key
    VIRUSTOTAL_API_KEY: Optional[str] = None
    VIRUSTOTAL_BASE_URL: str = "https://www.virustotal.com/api/v3"
    
    # Shodan API Key (optional)
    SHODAN_API_KEY: Optional[str] = None
    
    # ============================================
    # AI Models Configuration
    # ============================================
    
    AI_MODEL_PATH: str = "./models"
    HF_PHISHING_MODEL: str = "distilbert-base-uncased-finetuned-sst-2-english"
    MODEL_LOADING_STRATEGY: str = "startup"  # startup or lazy
    AI_DEVICE: str = "cpu"  # cpu, cuda, or mps
    
    # ============================================
    # Performance & Limits
    # ============================================
    
    MAX_FILE_SIZE_MB: int = 50
    RATE_LIMIT_PER_MINUTE: int = 60
    EXTERNAL_API_TIMEOUT: int = 30
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instance globale des settings
settings = Settings()


# Validation des clés API au démarrage
def validate_api_keys():
    """Valide que les clés API critiques sont présentes"""
    warnings = []
    
    if not settings.ABUSEIPDB_API_KEY:
        warnings.append("⚠️  ABUSEIPDB_API_KEY non configurée - Network Scan limité")
    
    if not settings.VIRUSTOTAL_API_KEY:
        warnings.append("⚠️  VIRUSTOTAL_API_KEY non configurée - Malware Analysis limité")
    
    if warnings:
        print("\n" + "="*60)
        print("⚠️  AVERTISSEMENT - Configuration API")
        print("="*60)
        for warning in warnings:
            print(warning)
        print("\nConfigurez les clés API dans le fichier .env")
        print("="*60 + "\n")
    else:
        print("✅ Toutes les clés API sont configurées")


# Export pour faciliter l'import
__all__ = ["settings", "validate_api_keys"]

