"""
AbuseIPDB API Client
Documentation: https://docs.abuseipdb.com/
"""
import httpx
from typing import Optional, Dict, Any
from app.core.config import settings


class AbuseIPDBClient:
    """Client pour l'API AbuseIPDB"""
    
    def __init__(self):
        self.base_url = settings.ABUSEIPDB_BASE_URL
        self.api_key = settings.ABUSEIPDB_API_KEY
        self.timeout = settings.EXTERNAL_API_TIMEOUT
    
    def _get_headers(self) -> Dict[str, str]:
        """Retourne les headers pour les requêtes API"""
        return {
            "Key": self.api_key,
            "Accept": "application/json"
        }
    
    async def check_ip(self, ip_address: str, max_age_days: int = 90) -> Optional[Dict[str, Any]]:
        """
        Vérifie la réputation d'une adresse IP
        
        Args:
            ip_address: Adresse IP à vérifier
            max_age_days: Nombre de jours d'historique (1-365)
        
        Returns:
            Dict contenant les informations de réputation ou None si erreur
        """
        if not self.api_key:
            print("⚠️ AbuseIPDB API Key non configurée")
            return None
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/check",
                    headers=self._get_headers(),
                    params={
                        "ipAddress": ip_address,
                        "maxAgeInDays": max_age_days,
                        "verbose": True
                    }
                )
                
                response.raise_for_status()
                data = response.json()
                
                if "data" in data:
                    return data["data"]
                
                return None
                
        except httpx.HTTPStatusError as e:
            print(f"❌ Erreur HTTP AbuseIPDB: {e.response.status_code}")
            if e.response.status_code == 401:
                print("   Clé API invalide")
            elif e.response.status_code == 429:
                print("   Rate limit dépassé")
            return None
        except httpx.TimeoutException:
            print(f"⏱️ Timeout lors de la requête AbuseIPDB")
            return None
        except Exception as e:
            print(f"❌ Erreur AbuseIPDB: {str(e)}")
            return None
    
    async def report_ip(
        self,
        ip_address: str,
        categories: list[int],
        comment: str
    ) -> bool:
        """
        Signale une IP malveillante (optionnel)
        
        Args:
            ip_address: IP à signaler
            categories: Liste des catégories (ex: [18, 22] pour SSH, Web)
            comment: Description de l'activité malveillante
        
        Returns:
            True si le signalement a réussi
        """
        if not self.api_key:
            return False
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/report",
                    headers=self._get_headers(),
                    data={
                        "ip": ip_address,
                        "categories": ",".join(map(str, categories)),
                        "comment": comment
                    }
                )
                
                response.raise_for_status()
                return True
                
        except Exception as e:
            print(f"❌ Erreur lors du signalement AbuseIPDB: {str(e)}")
            return False


# Instance singleton
abuseipdb_client = AbuseIPDBClient()


