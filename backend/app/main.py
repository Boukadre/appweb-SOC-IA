"""
Cyber IA Platform - FastAPI Backend
Point d'entrée principal de l'API
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings, validate_api_keys
from app.core.ai_manager import load_ai_models, unload_ai_models

from app.modules.network_scan.router import router as network_scan_router
from app.modules.malware_analysis.router import router as malware_router
from app.modules.phishing_detect.router import router as phishing_router
from app.modules.report_gen.router import router as report_router
from app.modules.cve_scanner.router import router as cve_scanner_router
from app.modules.password_analyzer.router import router as password_analyzer_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestion du cycle de vie de l'application
    - Startup: Charge les modèles IA et valide la config
    - Shutdown: Nettoie les ressources
    """
    # Startup
    print("\n" + "="*60)
    print("🚀 Démarrage de Cyber IA Platform")
    print("="*60)
    
    # Valider les clés API
    validate_api_keys()
    
    # Charger les modèles IA si configuré
    if settings.MODEL_LOADING_STRATEGY == "startup":
        await load_ai_models()
    else:
        print("⚠️  Chargement IA en mode 'lazy' - modèles chargés à la première requête")
    
    print("="*60)
    print("✅ Cyber IA Platform opérationnelle")
    print(f"📍 Environment: {settings.ENVIRONMENT}")
    print(f"🌐 CORS: {settings.ALLOWED_ORIGINS}")
    print("="*60 + "\n")
    
    yield
    
    # Shutdown
    print("\n" + "="*60)
    print("🛑 Arrêt de Cyber IA Platform")
    print("="*60)
    await unload_ai_models()
    print("✅ Ressources libérées")
    print("="*60 + "\n")


# Initialisation de l'application FastAPI avec lifespan
app = FastAPI(
    title="Cyber IA Platform API",
    description="API professionnelle pour l'analyse de sécurité cyber avec IA",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Configuration CORS pour autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes de santé et statut
@app.get("/", tags=["Health"])
async def root():
    """Endpoint racine - Status de l'API"""
    return {
        "status": "operational",
        "service": "Cyber IA Platform API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint pour monitoring"""
    return {
        "status": "healthy",
        "modules": {
            "network_scan": "active",
            "malware_analysis": "active",
            "phishing_detect": "active",
            "report_gen": "active",
            "cve_scanner": "active",
            "password_analyzer": "active"
        }
    }


# Inclusion des routers des différents modules
app.include_router(
    network_scan_router,
    prefix="/api/network-scan",
    tags=["Network Scan"]
)

app.include_router(
    malware_router,
    prefix="/api/malware-analysis",
    tags=["Malware Analysis"]
)

app.include_router(
    phishing_router,
    prefix="/api/phishing-detect",
    tags=["Phishing Detection"]
)

app.include_router(
    report_router,
    prefix="/api/report-gen",
    tags=["Report Generation"]
)

app.include_router(
    cve_scanner_router,
    prefix="/api/cve-scanner",
    tags=["CVE Scanner"]
)

app.include_router(
    password_analyzer_router,
    prefix="/api/password-analyzer",
    tags=["Password Analyzer"]
)


# Note: Les event handlers startup/shutdown sont remplacés par lifespan (FastAPI moderne)

