"""
Router pour le module Password Analyzer
Analyse de la force des mots de passe
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PasswordAnalyzeRequest, PasswordAnalyzeResponse
from app.modules.password_analyzer.service import PasswordAnalyzerService

router = APIRouter()
service = PasswordAnalyzerService()


@router.post("/analyze", response_model=PasswordAnalyzeResponse)
async def analyze_password(request: PasswordAnalyzeRequest):
    """
    Analyse la force d'un mot de passe
    
    - **password**: Mot de passe à analyser
    
    Retourne un score de 0 (très faible) à 4 (très fort)
    avec des suggestions d'amélioration
    """
    print(f"\n{'='*60}")
    print(f"📥 REQUEST RECEIVED:")
    print(f"   Password: {'*' * len(request.password)} ({len(request.password)} chars)")
    print(f"{'='*60}")
    
    try:
        # Validation stricte
        if not request.password or not isinstance(request.password, str):
            print("❌ ERROR: Password is empty or not a string")
            raise HTTPException(
                status_code=400,
                detail="Le mot de passe doit être une chaîne de caractères non vide"
            )
        
        # Trim
        password_trimmed = request.password.strip()
        
        if not password_trimmed:
            print("❌ ERROR: Password is empty after trim")
            raise HTTPException(
                status_code=400,
                detail="Le mot de passe ne peut pas être vide"
            )
        
        if len(password_trimmed) > 256:
            print(f"❌ ERROR: Password too long ({len(password_trimmed)} chars)")
            raise HTTPException(
                status_code=400,
                detail="Mot de passe trop long (max 256 caractères)"
            )
        
        print(f"✅ Validation OK, calling service...")
        
        # Appel du service
        result = await service.analyze_password(password_trimmed)
        
        print(f"✅ Analysis complete:")
        print(f"   Score: {result.score}/4")
        print(f"   Strength: {result.strength}")
        print(f"   Crack time: {result.crack_time_display}")
        print(f"{'='*60}\n")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR in router: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=400,
            detail=f"Erreur lors de l'analyse: {str(e)}"
        )
