"""
Router pour le module Network Scan
Gestion des endpoints de scan réseau et détection de vulnérabilités
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from app.models.schemas import (
    NetworkScanRequest,
    NetworkScanResponse,
    BaseResponse,
    ScanStatus,
    ThreatLevel
)
from app.modules.network_scan.service import NetworkScanService
from datetime import datetime
import uuid

router = APIRouter()
service = NetworkScanService()


@router.post("/start", response_model=NetworkScanResponse, status_code=202)
async def start_network_scan(
    request: NetworkScanRequest,
    background_tasks: BackgroundTasks
):
    """
    Démarre un scan réseau asynchrone
    
    - **target**: IP ou domaine à scanner
    - **scan_type**: Type de scan (quick, full, stealth)
    - **ports**: Ports spécifiques à scanner (optionnel)
    """
    try:
        # Génération d'un ID unique pour le scan
        scan_id = f"scan_{uuid.uuid4().hex[:8]}"
        
        # Validation de la cible
        if not request.target:
            raise HTTPException(status_code=400, detail="Target cannot be empty")
        
        # TODO: Ajouter la tâche de scan en background
        # background_tasks.add_task(service.perform_scan, scan_id, request)
        
        # Retour immédiat avec statut pending
        return NetworkScanResponse(
            scan_id=scan_id,
            status=ScanStatus.PENDING,
            target=request.target,
            open_ports=[],
            vulnerabilities=[],
            threat_level=ThreatLevel.LOW,
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du démarrage du scan: {str(e)}")


@router.get("/status/{scan_id}", response_model=NetworkScanResponse)
async def get_scan_status(scan_id: str):
    """
    Récupère le statut et les résultats d'un scan
    
    - **scan_id**: ID du scan à vérifier
    """
    try:
        result = await service.get_scan_result(scan_id)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Scan {scan_id} not found")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du scan: {str(e)}")


@router.get("/history", response_model=List[NetworkScanResponse])
async def get_scan_history(limit: int = 10, skip: int = 0):
    """
    Récupère l'historique des scans effectués
    
    - **limit**: Nombre de résultats à retourner
    - **skip**: Nombre de résultats à sauter (pagination)
    """
    try:
        history = await service.get_scan_history(limit=limit, skip=skip)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'historique: {str(e)}")


@router.delete("/{scan_id}", response_model=BaseResponse)
async def delete_scan(scan_id: str):
    """
    Supprime un scan de l'historique
    
    - **scan_id**: ID du scan à supprimer
    """
    try:
        success = await service.delete_scan(scan_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Scan {scan_id} not found")
        
        return BaseResponse(
            success=True,
            message=f"Scan {scan_id} supprimé avec succès"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression: {str(e)}")


@router.post("/quick-scan", response_model=NetworkScanResponse)
async def quick_scan(target: str):
    """
    Effectue un scan rapide synchrone (pour tests)
    
    - **target**: IP ou domaine à scanner
    """
    try:
        result = await service.quick_scan(target)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du scan rapide: {str(e)}")


@router.post("/ssh-audit")
async def analyze_ssh_logs(log_content: str):
    """
    Analyse des logs SSH/auth pour détecter les tentatives d'intrusion
    
    - **log_content**: Contenu du fichier auth.log ou secure (logs SSH)
    
    Retourne:
    - Statistiques d'attaques
    - Top des attaquants avec géolocalisation
    - Patterns d'attaque détectés
    - Recommandations de sécurité
    """
    try:
        if not log_content or len(log_content.strip()) == 0:
            raise HTTPException(
                status_code=400, 
                detail="Le contenu du log ne peut pas être vide"
            )
        
        if len(log_content) > 10_000_000:  # 10 MB max
            raise HTTPException(
                status_code=400,
                detail="Le fichier log est trop volumineux (max 10 MB)"
            )
        
        result = await service.analyze_ssh_logs(log_content)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de l'analyse des logs SSH: {str(e)}"
        )
