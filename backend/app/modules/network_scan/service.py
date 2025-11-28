"""
Service pour le module Network Scan
Logique métier pour les scans réseau et détection de vulnérabilités
"""
from typing import List, Optional, Dict, Any
import socket
import asyncio
from datetime import datetime
import uuid
import re
from collections import Counter

from app.models.schemas import NetworkScanResponse, ScanStatus, ThreatLevel
from app.modules.network_scan.abuseipdb_client import abuseipdb_client


class NetworkScanService:
    """Service de gestion des scans réseau"""
    
    def __init__(self):
        # TODO: Remplacer par une vraie DB
        self.scans_db = {}
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 8080, 8443]
    
    async def perform_scan(self, scan_id: str, target: str, scan_type: str = "quick"):
        """
        Effectue un scan réseau complet (appelé en background)
        
        TODO: Implémenter la logique IA de scan réseau
        - Intégration avec nmap ou scapy
        - Analyse des ports ouverts
        - Détection de vulnérabilités connues (CVE)
        - Scoring de menace avec modèle IA
        """
        pass
    
    async def get_scan_result(self, scan_id: str) -> Optional[NetworkScanResponse]:
        """Récupère les résultats d'un scan"""
        # TODO: Récupérer depuis la DB
        return self.scans_db.get(scan_id)
    
    async def get_scan_history(self, limit: int = 10, skip: int = 0) -> List[NetworkScanResponse]:
        """Récupère l'historique des scans"""
        # TODO: Récupérer depuis la DB avec pagination
        return []
    
    async def delete_scan(self, scan_id: str) -> bool:
        """Supprime un scan"""
        # TODO: Supprimer de la DB
        if scan_id in self.scans_db:
            del self.scans_db[scan_id]
            return True
        return False
    
    async def quick_scan(self, target: str) -> NetworkScanResponse:
        """
        Scan rapide avec détection de ports et intégration AbuseIPDB
        """
        scan_id = f"scan_{uuid.uuid4().hex[:8]}"
        
        try:
            # Résoudre le domaine en IP si nécessaire
            ip_address = await self._resolve_target(target)
            
            # Scanner les ports communs
            open_ports = await self._scan_ports(ip_address, self.common_ports)
            
            # Analyser la réputation de l'IP via AbuseIPDB
            ip_reputation = await abuseipdb_client.check_ip(ip_address)
            
            # Identifier les vulnérabilités
            vulnerabilities = self._identify_vulnerabilities(open_ports, ip_reputation)
            
            # Calculer le niveau de menace
            threat_level = self._calculate_threat_level(open_ports, vulnerabilities, ip_reputation)
            
            result = NetworkScanResponse(
                scan_id=scan_id,
                status=ScanStatus.COMPLETED,
                target=target,
                open_ports=open_ports,
                vulnerabilities=vulnerabilities,
                threat_level=threat_level,
                timestamp=datetime.utcnow()
            )
            
            self.scans_db[scan_id] = result
            return result
            
        except Exception as e:
            print(f"❌ Erreur lors du scan: {str(e)}")
            # Retourner un résultat d'erreur
            result = NetworkScanResponse(
                scan_id=scan_id,
                status=ScanStatus.FAILED,
                target=target,
                open_ports=[],
                vulnerabilities=[{
                    "port": 0,
                    "service": "error",
                    "description": f"Scan failed: {str(e)}",
                    "severity": "low"
                }],
                threat_level=ThreatLevel.LOW,
                timestamp=datetime.utcnow()
            )
            self.scans_db[scan_id] = result
            return result
    
    async def _resolve_target(self, target: str) -> str:
        """Résout un domaine en adresse IP"""
        # Vérifier si c'est déjà une IP
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
            return target
        
        # Résoudre le domaine
        try:
            # Retirer http(s):// si présent
            target = re.sub(r'^https?://', '', target)
            target = target.split('/')[0]  # Retirer le path
            
            ip = socket.gethostbyname(target)
            print(f"🔍 Résolu {target} → {ip}")
            return ip
        except socket.gaierror:
            print(f"⚠️ Impossible de résoudre {target}")
            return target
    
    async def _scan_ports(self, ip: str, ports: List[int]) -> List[int]:
        """Scanne une liste de ports (scan TCP basique)"""
        open_ports = []
        
        async def check_port(port: int) -> bool:
            """Vérifie si un port est ouvert"""
            try:
                # Timeout de 1 seconde par port
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, port),
                    timeout=1.0
                )
                writer.close()
                await writer.wait_closed()
                return True
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                return False
        
        # Scanner tous les ports en parallèle
        tasks = [check_port(port) for port in ports]
        results = await asyncio.gather(*tasks)
        
        # Collecter les ports ouverts
        open_ports = [port for port, is_open in zip(ports, results) if is_open]
        
        print(f"🔓 Ports ouverts sur {ip}: {open_ports}")
        return open_ports
    
    def _identify_vulnerabilities(
        self,
        open_ports: List[int],
        ip_reputation: Optional[dict]
    ) -> List[dict]:
        """Identifie les vulnérabilités potentielles"""
        vulnerabilities = []
        
        # Port-based vulnerabilities
        port_vulns = {
            21: {"service": "FTP", "description": "FTP service detected - unencrypted protocol", "severity": "medium"},
            22: {"service": "SSH", "description": "SSH exposed - ensure strong authentication", "severity": "low"},
            23: {"service": "Telnet", "description": "Telnet detected - critical security risk (unencrypted)", "severity": "high"},
            25: {"service": "SMTP", "description": "SMTP server exposed", "severity": "low"},
            3306: {"service": "MySQL", "description": "MySQL database publicly accessible", "severity": "high"},
            3389: {"service": "RDP", "description": "Remote Desktop exposed - high attack surface", "severity": "high"},
            8080: {"service": "HTTP-Alt", "description": "Alternative HTTP port - may lack encryption", "severity": "medium"},
        }
        
        for port in open_ports:
            if port in port_vulns:
                vuln = port_vulns[port].copy()
                vuln["port"] = port
                vulnerabilities.append(vuln)
        
        # AbuseIPDB reputation-based vulnerabilities
        if ip_reputation:
            abuse_score = ip_reputation.get("abuseConfidenceScore", 0)
            if abuse_score > 75:
                vulnerabilities.append({
                    "port": 0,
                    "service": "reputation",
                    "description": f"IP has high abuse score: {abuse_score}% (AbuseIPDB)",
                    "severity": "critical"
                })
            elif abuse_score > 50:
                vulnerabilities.append({
                    "port": 0,
                    "service": "reputation",
                    "description": f"IP has moderate abuse score: {abuse_score}% (AbuseIPDB)",
                    "severity": "high"
                })
            elif abuse_score > 0:
                vulnerabilities.append({
                    "port": 0,
                    "service": "reputation",
                    "description": f"IP has been reported for abuse: {abuse_score}% confidence",
                    "severity": "medium"
                })
        
        return vulnerabilities
    
    def _calculate_threat_level(
        self,
        open_ports: List[int],
        vulnerabilities: List[dict],
        ip_reputation: Optional[dict]
    ) -> ThreatLevel:
        """Calcule le niveau de menace global"""
        # Compter les vulnérabilités par sévérité
        critical = sum(1 for v in vulnerabilities if v.get("severity") == "critical")
        high = sum(1 for v in vulnerabilities if v.get("severity") == "high")
        medium = sum(1 for v in vulnerabilities if v.get("severity") == "medium")
        
        # Score AbuseIPDB
        abuse_score = 0
        if ip_reputation:
            abuse_score = ip_reputation.get("abuseConfidenceScore", 0)
        
        # Logique de décision
        if critical > 0 or abuse_score > 75:
            return ThreatLevel.CRITICAL
        elif high >= 2 or abuse_score > 50:
            return ThreatLevel.HIGH
        elif high > 0 or medium >= 2 or abuse_score > 25:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    # ============= SSH LOG FORENSICS =============
    
    async def analyze_ssh_logs(self, log_content: str) -> Dict[str, Any]:
        """
        Analyse les logs SSH pour détecter les tentatives d'intrusion
        
        Args:
            log_content: Contenu du fichier auth.log ou secure
            
        Returns:
            Dictionnaire contenant les statistiques d'attaques SSH
        """
        analysis_id = f"ssh_audit_{uuid.uuid4().hex[:8]}"
        
        # Parser les logs pour extraire les IPs avec échecs d'authentification
        failed_ips = self._parse_auth_log(log_content)
        
        if not failed_ips:
            return {
                "analysis_id": analysis_id,
                "total_attacks": 0,
                "unique_attackers": 0,
                "top_attackers": [],
                "attack_patterns": [],
                "recommendations": ["Aucune tentative d'attaque détectée dans les logs fournis"],
                "threat_level": ThreatLevel.LOW,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Compter les occurrences par IP
        ip_counter = Counter(failed_ips)
        total_attacks = len(failed_ips)
        unique_attackers = len(ip_counter)
        
        # Top 10 des attaquants
        top_attackers = []
        for ip, count in ip_counter.most_common(10):
            attacker_info = {
                "ip": ip,
                "attempts": count,
                "percentage": round((count / total_attacks) * 100, 2),
            }
            
            # Enrichir avec AbuseIPDB si possible
            try:
                ip_reputation = await abuseipdb_client.check_ip(ip)
                if ip_reputation:
                    attacker_info["abuse_score"] = ip_reputation.get("abuseConfidenceScore", 0)
                    attacker_info["country"] = ip_reputation.get("countryCode", "Unknown")
                    attacker_info["is_whitelisted"] = ip_reputation.get("isWhitelisted", False)
            except Exception as e:
                print(f"⚠️ Erreur lors de la vérification de {ip}: {str(e)}")
                attacker_info["abuse_score"] = None
                attacker_info["country"] = "Unknown"
            
            top_attackers.append(attacker_info)
        
        # Détecter les patterns d'attaque
        attack_patterns = self._detect_attack_patterns(failed_ips, ip_counter)
        
        # Calculer le niveau de menace
        threat_level = self._calculate_ssh_threat_level(
            total_attacks, 
            unique_attackers, 
            ip_counter,
            top_attackers
        )
        
        # Générer des recommandations
        recommendations = self._generate_ssh_recommendations(
            total_attacks, 
            unique_attackers, 
            threat_level,
            top_attackers
        )
        
        return {
            "analysis_id": analysis_id,
            "total_attacks": total_attacks,
            "unique_attackers": unique_attackers,
            "top_attackers": top_attackers,
            "attack_patterns": attack_patterns,
            "recommendations": recommendations,
            "threat_level": threat_level,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _parse_auth_log(self, log_content: str) -> List[str]:
        """
        Parse les logs d'authentification pour extraire les IPs avec échecs
        
        Patterns supportés:
        - Failed password for ...
        - authentication failure...
        - Invalid user ...
        """
        failed_ips = []
        
        # Patterns regex pour détecter les échecs d'authentification
        patterns = [
            r'Failed password for .* from ([\d\.]+)',
            r'authentication failure.*rhost=([\d\.]+)',
            r'Invalid user .* from ([\d\.]+)',
            r'Connection closed by authenticating user .* ([\d\.]+)',
            r'Disconnected from authenticating user .* ([\d\.]+)',
            r'Failed publickey for .* from ([\d\.]+)',
            r'fatal: Unable to negotiate .* from ([\d\.]+)',
        ]
        
        for line in log_content.split('\n'):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    ip = match.group(1)
                    # Valider que c'est bien une IP
                    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
                        failed_ips.append(ip)
                    break  # Une seule correspondance par ligne
        
        return failed_ips
    
    def _detect_attack_patterns(self, failed_ips: List[str], ip_counter: Counter) -> List[Dict[str, Any]]:
        """Détecte les patterns d'attaque (brute force, distributed, etc.)"""
        patterns = []
        
        # Pattern 1: Brute Force massif (une IP avec beaucoup de tentatives)
        max_attempts = ip_counter.most_common(1)[0][1] if ip_counter else 0
        if max_attempts > 100:
            patterns.append({
                "type": "brute_force",
                "description": f"Attaque par force brute détectée ({max_attempts} tentatives depuis une seule IP)",
                "severity": "high"
            })
        elif max_attempts > 50:
            patterns.append({
                "type": "brute_force",
                "description": f"Tentatives répétées de connexion ({max_attempts} depuis une IP)",
                "severity": "medium"
            })
        
        # Pattern 2: Attaque distribuée (beaucoup d'IPs différentes)
        unique_count = len(ip_counter)
        if unique_count > 50:
            patterns.append({
                "type": "distributed",
                "description": f"Attaque distribuée détectée ({unique_count} IPs différentes)",
                "severity": "high"
            })
        elif unique_count > 20:
            patterns.append({
                "type": "distributed",
                "description": f"Attaque potentiellement distribuée ({unique_count} IPs)",
                "severity": "medium"
            })
        
        # Pattern 3: Scan de réseau (beaucoup d'IPs avec peu de tentatives chacune)
        low_attempt_ips = sum(1 for count in ip_counter.values() if count <= 3)
        if low_attempt_ips > 10 and low_attempt_ips / unique_count > 0.5:
            patterns.append({
                "type": "network_scan",
                "description": f"Scan de réseau détecté ({low_attempt_ips} IPs avec peu de tentatives)",
                "severity": "low"
            })
        
        if not patterns:
            patterns.append({
                "type": "normal",
                "description": "Tentatives d'authentification normales",
                "severity": "low"
            })
        
        return patterns
    
    def _calculate_ssh_threat_level(
        self, 
        total_attacks: int, 
        unique_attackers: int,
        ip_counter: Counter,
        top_attackers: List[Dict[str, Any]]
    ) -> ThreatLevel:
        """Calcule le niveau de menace basé sur l'analyse SSH"""
        
        # Vérifier si des IPs ont un score d'abuse élevé
        high_abuse_count = sum(
            1 for attacker in top_attackers 
            if attacker.get("abuse_score", 0) > 75
        )
        
        # Logique de décision
        if total_attacks > 1000 or high_abuse_count >= 3:
            return ThreatLevel.CRITICAL
        elif total_attacks > 500 or unique_attackers > 50 or high_abuse_count >= 1:
            return ThreatLevel.HIGH
        elif total_attacks > 100 or unique_attackers > 10:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def _generate_ssh_recommendations(
        self,
        total_attacks: int,
        unique_attackers: int,
        threat_level: ThreatLevel,
        top_attackers: List[Dict[str, Any]]
    ) -> List[str]:
        """Génère des recommandations de sécurité basées sur l'analyse"""
        recommendations = []
        
        if threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            recommendations.append("🔴 URGENT: Bloquez immédiatement les IPs suspectes avec fail2ban ou iptables")
            recommendations.append("🔐 Désactivez l'authentification par mot de passe et utilisez uniquement les clés SSH")
        
        if total_attacks > 100:
            recommendations.append("🛡️ Installez et configurez fail2ban pour bloquer automatiquement les attaquants")
            recommendations.append("🚪 Changez le port SSH par défaut (22) vers un port non-standard")
        
        if unique_attackers > 20:
            recommendations.append("🌍 Limitez l'accès SSH aux IPs/pays de confiance avec un firewall")
        
        # Recommandations générales
        recommendations.append("✓ Utilisez des clés SSH avec passphrase au lieu de mots de passe")
        recommendations.append("✓ Désactivez la connexion root directe (PermitRootLogin no)")
        recommendations.append("✓ Activez l'authentification à deux facteurs (2FA) pour SSH")
        recommendations.append("✓ Surveillez régulièrement vos logs avec des outils comme OSSEC ou Wazuh")
        
        # Recommandations spécifiques aux top attackers
        high_abuse_ips = [
            attacker["ip"] for attacker in top_attackers 
            if attacker.get("abuse_score", 0) > 50
        ]
        if high_abuse_ips:
            recommendations.append(
                f"⚠️ Bloquez ces IPs malveillantes connues: {', '.join(high_abuse_ips[:5])}"
            )
        
        return recommendations

