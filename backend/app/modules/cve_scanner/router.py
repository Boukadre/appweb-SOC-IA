"""
Router pour le module CVE Scanner
Détection de technologies et vulnérabilités CVE
"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import (
    CVEScanRequest,
    CVEScanResponse,
    BaseResponse
)
from app.modules.cve_scanner.service import CVEScannerService

router = APIRouter()
service = CVEScannerService()


@router.post("/scan", response_model=CVEScanResponse)
async def scan_website(request: CVEScanRequest):
    """
    Scanne un site web pour détecter les technologies et CVEs
    
    - **url**: URL du site à analyser
    - **deep_scan**: Analyse approfondie (plus lente)
    """
    try:
        if not request.url.startswith(("http://", "https://")):
            raise HTTPException(
                status_code=400,
                detail="URL invalide. Doit commencer par http:// ou https://"
            )
        
        result = await service.scan_website(request.url, request.deep_scan)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du scan: {str(e)}"
        )


@router.get("/history", response_model=List[CVEScanResponse])
async def get_scan_history(limit: int = 10):
    """Récupère l'historique des scans CVE"""
    try:
        history = await service.get_history(limit=limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.get("/{scan_id}", response_model=CVEScanResponse)
async def get_scan_result(scan_id: str):
    """Récupère les résultats d'un scan spécifique"""
    try:
        result = await service.get_scan(scan_id)
        if not result:
            raise HTTPException(status_code=404, detail="Scan non trouvé")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")



