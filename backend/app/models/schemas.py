"""
Modèles Pydantic pour la validation des données
Schémas pour les requêtes et réponses API
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============= ENUMS =============

class ScanStatus(str, Enum):
    """Statuts possibles pour une analyse"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ThreatLevel(str, Enum):
    """Niveaux de menace"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============= SCHEMAS COMMUNS =============

class BaseResponse(BaseModel):
    """Réponse API standard"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Réponse d'erreur standard"""
    error: str
    detail: Optional[str] = None
    code: Optional[int] = None


# ============= NETWORK SCAN =============

class NetworkScanRequest(BaseModel):
    """Requête pour un scan réseau"""
    target: str = Field(..., description="IP ou domaine cible")
    scan_type: str = Field(default="quick", description="Type de scan: quick, full, stealth")
    ports: Optional[str] = Field(None, description="Ports à scanner (ex: 80,443,8080)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "target": "192.168.1.1",
                "scan_type": "quick",
                "ports": "80,443,8080"
            }
        }


class NetworkScanResponse(BaseModel):
    """Réponse d'un scan réseau"""
    scan_id: str
    status: ScanStatus
    target: str
    open_ports: List[int]
    vulnerabilities: List[Dict[str, Any]]
    threat_level: ThreatLevel
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "scan_id": "scan_abc123",
                "status": "completed",
                "target": "192.168.1.1",
                "open_ports": [80, 443],
                "vulnerabilities": [],
                "threat_level": "low",
                "timestamp": "2025-11-27T10:00:00"
            }
        }


# ============= MALWARE ANALYSIS =============

class MalwareAnalysisRequest(BaseModel):
    """Requête pour analyse de malware"""
    file_hash: Optional[str] = Field(None, description="Hash du fichier")
    file_name: str = Field(..., description="Nom du fichier")
    analysis_depth: str = Field(default="standard", description="Profondeur: quick, standard, deep")


class MalwareAnalysisResponse(BaseModel):
    """Réponse d'analyse de malware"""
    analysis_id: str
    file_name: str
    is_malicious: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    threat_type: Optional[str] = None
    indicators: List[str]
    threat_level: ThreatLevel
    timestamp: datetime


# ============= PHISHING DETECTION =============

class PhishingDetectRequest(BaseModel):
    """Requête pour détection de phishing avec analyse complète d'email"""
    sender: Optional[str] = Field(None, description="Adresse email de l'expéditeur")
    subject: Optional[str] = Field(None, description="Objet de l'email")
    body: Optional[str] = Field(None, description="Corps du message email")
    url: Optional[str] = Field(None, description="URL à analyser (optionnel)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "sender": "support@paypal-secure.com",
                "subject": "Urgent: Votre compte sera suspendu",
                "body": "Cliquez ici pour vérifier votre compte...",
                "url": "https://paypal-secure.com/verify"
            }
        }


class PhishingDetectResponse(BaseModel):
    """Réponse de détection de phishing"""
    detection_id: str
    is_phishing: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    threat_category: str = Field(..., description="safe, suspicious, phishing")
    indicators: List[str]
    threat_level: ThreatLevel
    recommendations: List[str]
    ai_model_used: str = Field(..., description="Nom du modèle IA utilisé")
    timestamp: datetime


# ============= REPORT GENERATION =============

class ReportGenerationRequest(BaseModel):
    """Requête pour génération de rapport"""
    report_type: str = Field(..., description="Type: network_scan, malware, phishing, comprehensive")
    analysis_ids: List[str] = Field(..., description="IDs des analyses à inclure")
    format: str = Field(default="pdf", description="Format: pdf, html, json")
    include_recommendations: bool = Field(default=True)


class ReportGenerationResponse(BaseModel):
    """Réponse de génération de rapport"""
    report_id: str
    report_url: str
    format: str
    generated_at: datetime
    file_size_kb: int


# ============= CVE SCANNER =============

class CVEScanRequest(BaseModel):
    """Requête pour scan CVE"""
    url: str = Field(..., description="URL du site à analyser")
    deep_scan: bool = Field(default=False, description="Analyse approfondie")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "deep_scan": False
            }
        }


class TechnologyInfo(BaseModel):
    """Information sur une technologie détectée"""
    name: str
    version: Optional[str] = None
    category: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class CVEInfo(BaseModel):
    """Information sur une CVE"""
    cve_id: str
    description: str
    severity: ThreatLevel
    cvss_score: float
    affected_versions: List[str]
    patch_available: bool
    published_date: str


class CVEScanResponse(BaseModel):
    """Réponse de scan CVE"""
    scan_id: str
    url: str
    technologies: List[TechnologyInfo]
    vulnerabilities: List[CVEInfo]
    overall_risk: ThreatLevel
    total_cves: int
    timestamp: datetime


# ============= PASSWORD ANALYZER =============

class PasswordAnalyzeRequest(BaseModel):
    """Requête pour analyse de mot de passe"""
    password: str = Field(..., description="Mot de passe à analyser")
    
    class Config:
        json_schema_extra = {
            "example": {
                "password": "MyP@ssw0rd123"
            }
        }


class PasswordAnalyzeResponse(BaseModel):
    """Réponse d'analyse de mot de passe"""
    score: int = Field(..., ge=0, le=4, description="Score de 0 (faible) à 4 (fort)")
    strength: str = Field(..., description="Niveau: very_weak, weak, fair, strong, very_strong")
    crack_time_seconds: float
    crack_time_display: str
    entropy: float
    suggestions: List[str]
    warning: Optional[str] = None
    feedback: Dict[str, Any]
    timestamp: datetime
