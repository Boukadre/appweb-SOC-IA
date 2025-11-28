"""
Service pour le module CVE Scanner
Détection de technologies et recherche de CVEs
"""
from typing import List, Optional
import requests
from datetime import datetime
import uuid
import re
from urllib.parse import urlparse
import builtwith

from app.models.schemas import (
    CVEScanResponse,
    TechnologyInfo,
    CVEInfo,
    ThreatLevel
)


class CVEScannerService:
    """Service de scan CVE et détection de technologies"""
    
    def __init__(self):
        self.scan_db = {}
        # Base de données CVE simulée pour WordPress
        self.known_cves = {
            "WordPress": [
                {
                    "version_range": ["4.0", "6.0"],
                    "cve_id": "CVE-2023-2745",
                    "description": "WordPress Core XSS Vulnerability",
                    "severity": ThreatLevel.HIGH,
                    "cvss_score": 7.2,
                    "patch_available": True,
                    "published_date": "2023-05-16"
                },
                {
                    "version_range": ["3.0", "5.8"],
                    "cve_id": "CVE-2022-21661",
                    "description": "SQL Injection in WP_Query",
                    "severity": ThreatLevel.CRITICAL,
                    "cvss_score": 9.8,
                    "patch_available": True,
                    "published_date": "2022-01-06"
                }
            ],
            "Apache": [
                {
                    "version_range": ["2.4.0", "2.4.49"],
                    "cve_id": "CVE-2021-41773",
                    "description": "Path Traversal and RCE",
                    "severity": ThreatLevel.CRITICAL,
                    "cvss_score": 9.8,
                    "patch_available": True,
                    "published_date": "2021-10-05"
                }
            ],
            "nginx": [
                {
                    "version_range": ["1.0.0", "1.20.0"],
                    "cve_id": "CVE-2021-23017",
                    "description": "Off-by-one in resolver",
                    "severity": ThreatLevel.MEDIUM,
                    "cvss_score": 6.5,
                    "patch_available": True,
                    "published_date": "2021-05-25"
                }
            ],
            "jQuery": [
                {
                    "version_range": ["1.0.0", "3.4.0"],
                    "cve_id": "CVE-2020-11023",
                    "description": "XSS in jQuery HTML parsing",
                    "severity": ThreatLevel.MEDIUM,
                    "cvss_score": 6.1,
                    "patch_available": True,
                    "published_date": "2020-04-29"
                }
            ]
        }
    
    async def scan_website(self, url: str, deep_scan: bool = False) -> CVEScanResponse:
        """
        Scanne un site web pour détecter technologies et CVEs
        """
        scan_id = f"cve_{uuid.uuid4().hex[:8]}"
        
        try:
            # Détection des technologies avec builtwith
            technologies = await self._detect_technologies(url)
            
            # Détection via headers HTTP
            headers_tech = await self._analyze_headers(url)
            technologies.extend(headers_tech)
            
            # Recherche de CVEs pour les technologies détectées
            vulnerabilities = await self._find_cves(technologies)
            
            # Calcul du risque global
            overall_risk = self._calculate_overall_risk(vulnerabilities)
            
            result = CVEScanResponse(
                scan_id=scan_id,
                url=url,
                technologies=technologies,
                vulnerabilities=vulnerabilities,
                overall_risk=overall_risk,
                total_cves=len(vulnerabilities),
                timestamp=datetime.utcnow()
            )
            
            self.scan_db[scan_id] = result
            return result
            
        except Exception as e:
            # En cas d'erreur, retourne un résultat minimal
            result = CVEScanResponse(
                scan_id=scan_id,
                url=url,
                technologies=[],
                vulnerabilities=[],
                overall_risk=ThreatLevel.LOW,
                total_cves=0,
                timestamp=datetime.utcnow()
            )
            self.scan_db[scan_id] = result
            return result
    
    async def _detect_technologies(self, url: str) -> List[TechnologyInfo]:
        """Détecte les technologies avec builtwith"""
        technologies = []
        
        try:
            info = builtwith.parse(url)
            
            # Mapping des catégories builtwith
            for category, techs in info.items():
                for tech in techs:
                    # Extraire version si présente
                    version_match = re.search(r'(\d+\.[\d.]+)', tech)
                    version = version_match.group(1) if version_match else None
                    tech_name = re.sub(r'\s*\d+\.[\d.]+\s*', '', tech).strip()
                    
                    technologies.append(TechnologyInfo(
                        name=tech_name,
                        version=version,
                        category=category,
                        confidence=0.9
                    ))
        except Exception as e:
            print(f"Erreur builtwith: {e}")
        
        return technologies
    
    async def _analyze_headers(self, url: str) -> List[TechnologyInfo]:
        """Analyse les headers HTTP pour détecter serveur et technologies"""
        technologies = []
        
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Cyber IA Platform Scanner)'
            })
            
            headers = response.headers
            
            # Détection du serveur
            if 'Server' in headers:
                server = headers['Server']
                version_match = re.search(r'(\d+\.[\d.]+)', server)
                version = version_match.group(1) if version_match else None
                server_name = re.sub(r'[/\d.]', '', server).strip()
                
                technologies.append(TechnologyInfo(
                    name=server_name,
                    version=version,
                    category="Web Server",
                    confidence=1.0
                ))
            
            # Détection PHP
            if 'X-Powered-By' in headers:
                powered_by = headers['X-Powered-By']
                if 'PHP' in powered_by:
                    version_match = re.search(r'(\d+\.[\d.]+)', powered_by)
                    version = version_match.group(1) if version_match else None
                    
                    technologies.append(TechnologyInfo(
                        name="PHP",
                        version=version,
                        category="Programming Language",
                        confidence=1.0
                    ))
            
            # Détection WordPress via body
            if 'wp-content' in response.text or 'wp-includes' in response.text:
                # Chercher la version WordPress
                version_match = re.search(r'wp-includes/js/[^/]+\?ver=([\d.]+)', response.text)
                version = version_match.group(1) if version_match else None
                
                technologies.append(TechnologyInfo(
                    name="WordPress",
                    version=version,
                    category="CMS",
                    confidence=0.95
                ))
            
        except Exception as e:
            print(f"Erreur analyse headers: {e}")
        
        return technologies
    
    async def _find_cves(self, technologies: List[TechnologyInfo]) -> List[CVEInfo]:
        """Recherche les CVEs pour les technologies détectées"""
        vulnerabilities = []
        
        for tech in technologies:
            if tech.name in self.known_cves:
                cves_for_tech = self.known_cves[tech.name]
                
                for cve_data in cves_for_tech:
                    # Si on a une version, vérifier si elle est vulnérable
                    if tech.version:
                        is_vulnerable = self._is_version_vulnerable(
                            tech.version,
                            cve_data["version_range"]
                        )
                        if not is_vulnerable:
                            continue
                    
                    vulnerabilities.append(CVEInfo(
                        cve_id=cve_data["cve_id"],
                        description=cve_data["description"],
                        severity=cve_data["severity"],
                        cvss_score=cve_data["cvss_score"],
                        affected_versions=cve_data["version_range"],
                        patch_available=cve_data["patch_available"],
                        published_date=cve_data["published_date"]
                    ))
        
        return vulnerabilities
    
    def _is_version_vulnerable(self, version: str, version_range: List[str]) -> bool:
        """Vérifie si une version est dans la plage vulnérable"""
        try:
            version_parts = [int(x) for x in version.split('.')]
            min_parts = [int(x) for x in version_range[0].split('.')]
            max_parts = [int(x) for x in version_range[1].split('.')]
            
            return min_parts <= version_parts <= max_parts
        except:
            return True  # En cas de doute, considérer comme vulnérable
    
    def _calculate_overall_risk(self, vulnerabilities: List[CVEInfo]) -> ThreatLevel:
        """Calcule le niveau de risque global"""
        if not vulnerabilities:
            return ThreatLevel.LOW
        
        # Compter les vulnérabilités par sévérité
        critical_count = sum(1 for v in vulnerabilities if v.severity == ThreatLevel.CRITICAL)
        high_count = sum(1 for v in vulnerabilities if v.severity == ThreatLevel.HIGH)
        
        if critical_count > 0:
            return ThreatLevel.CRITICAL
        elif high_count >= 2:
            return ThreatLevel.HIGH
        elif high_count > 0 or len(vulnerabilities) >= 3:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    async def get_history(self, limit: int = 10) -> List[CVEScanResponse]:
        """Récupère l'historique des scans"""
        return list(self.scan_db.values())[:limit]
    
    async def get_scan(self, scan_id: str) -> Optional[CVEScanResponse]:
        """Récupère un scan spécifique"""
        return self.scan_db.get(scan_id)


