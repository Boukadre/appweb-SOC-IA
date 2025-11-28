"""
Router pour le module Report Generation
Gestion des endpoints de génération de rapports
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List
from app.models.schemas import (
    ReportGenerationRequest,
    ReportGenerationResponse,
    BaseResponse
)
from app.modules.report_gen.service import ReportGenerationService
from datetime import datetime
import uuid

router = APIRouter()
service = ReportGenerationService()


@router.post("/generate", response_model=ReportGenerationResponse, status_code=202)
async def generate_report(request: ReportGenerationRequest):
    """
    Génère un rapport consolidé des analyses
    
    - **report_type**: Type de rapport (network_scan, malware, phishing, comprehensive)
    - **analysis_ids**: Liste des IDs d'analyses à inclure
    - **format**: Format du rapport (pdf, html, json)
    - **include_recommendations**: Inclure les recommandations
    """
    try:
        if not request.analysis_ids:
            raise HTTPException(
                status_code=400,
                detail="Au moins un ID d'analyse est requis"
            )
        
        result = await service.generate_report(request)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération: {str(e)}")


@router.get("/status/{report_id}", response_model=ReportGenerationResponse)
async def get_report_status(report_id: str):
    """
    Récupère le statut de génération d'un rapport
    
    - **report_id**: ID du rapport
    """
    try:
        result = await service.get_report_status(report_id)
        if not result:
            raise HTTPException(status_code=404, detail="Rapport non trouvé")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.get("/download/{report_id}")
async def download_report(report_id: str):
    """
    Télécharge un rapport généré
    
    - **report_id**: ID du rapport à télécharger
    """
    try:
        file_path = await service.get_report_file(report_id)
        if not file_path:
            raise HTTPException(status_code=404, detail="Rapport non trouvé")
        
        # TODO: Retourner le fichier réel
        raise HTTPException(status_code=501, detail="Download not implemented yet")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.get("/history", response_model=List[ReportGenerationResponse])
async def get_report_history(limit: int = 10):
    """Récupère l'historique des rapports générés"""
    try:
        history = await service.get_history(limit=limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.delete("/{report_id}", response_model=BaseResponse)
async def delete_report(report_id: str):
    """Supprime un rapport"""
    try:
        success = await service.delete_report(report_id)
        if not success:
            raise HTTPException(status_code=404, detail="Rapport non trouvé")
        
        return BaseResponse(
            success=True,
            message=f"Rapport {report_id} supprimé avec succès"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

