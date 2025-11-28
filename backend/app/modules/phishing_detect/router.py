"""
Router pour le module Phishing Detection
Gestion des endpoints de détection de phishing avec modèle BERT
"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import (
    PhishingDetectRequest,
    PhishingDetectResponse,
    BaseResponse,
    ThreatLevel
)
from app.modules.phishing_detect.service import PhishingDetectService
from datetime import datetime
import uuid

router = APIRouter()
service = PhishingDetectService()


@router.post("/analyze", response_model=PhishingDetectResponse)
async def detect_phishing(request: PhishingDetectRequest):
    """
    Analyse complète d'un email avec modèle BERT
    
    Champs supportés:
    - **sender**: Adresse email de l'expéditeur (ex: support@paypal.com)
    - **subject**: Objet de l'email (ex: "Urgent: Verify your account")
    - **body**: Corps du message email
    - **url**: URL à analyser (optionnel)
    
    Le modèle BERT concatène intelligemment ces champs pour l'analyse.
    
    Retourne:
    - **is_phishing**: true/false
    - **confidence**: Score de 0 à 1
    - **threat_category**: "safe", "suspicious", ou "phishing"
    - **threat_level**: LOW, MEDIUM, HIGH, CRITICAL
    - **indicators**: Liste des indicateurs détectés
    - **recommendations**: Actions recommandées
    """
    try:
        # Validation : au moins un champ doit être fourni
        if not any([request.sender, request.subject, request.body, request.url]):
            raise HTTPException(
                status_code=400,
                detail="Au moins un champ est requis (sender, subject, body, ou url)"
            )
        
        result = await service.analyze_phishing(request)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de l'analyse: {str(e)}"
        )


@router.post("/analyze-url", response_model=PhishingDetectResponse)
async def analyze_url(url: str):
    """
    Analyse rapide d'une URL (rétrocompatibilité)
    
    - **url**: URL à analyser
    """
    try:
        request = PhishingDetectRequest(url=url)
        result = await service.analyze_phishing(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de l'analyse: {str(e)}"
        )


@router.post("/analyze-email", response_model=PhishingDetectResponse)
async def analyze_email(
    sender: str = None,
    subject: str = None,
    body: str = None
):
    """
    Analyse d'email avec champs séparés (rétrocompatibilité)
    
    - **sender**: Adresse de l'expéditeur
    - **subject**: Objet de l'email
    - **body**: Corps du message
    """
    try:
        if not any([sender, subject, body]):
            raise HTTPException(
                status_code=400,
                detail="Au moins un champ requis (sender, subject, ou body)"
            )
        
        request = PhishingDetectRequest(
            sender=sender,
            subject=subject,
            body=body
        )
        result = await service.analyze_phishing(request)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de l'analyse: {str(e)}"
        )


@router.get("/history", response_model=List[PhishingDetectResponse])
async def get_detection_history(limit: int = 10):
    """
    Récupère l'historique des détections
    
    - **limit**: Nombre de résultats à retourner (défaut: 10)
    """
    try:
        history = await service.get_history(limit=limit)
        return history
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur: {str(e)}"
        )


@router.get("/{detection_id}", response_model=PhishingDetectResponse)
async def get_detection_result(detection_id: str):
    """
    Récupère les résultats d'une détection spécifique
    
    - **detection_id**: ID de la détection
    """
    try:
        result = await service.get_detection(detection_id)
        if not result:
            raise HTTPException(
                status_code=404, 
                detail="Détection non trouvée"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur: {str(e)}"
        )
