"""
Service pour le module Phishing Detection
Détection de phishing HYBRIDE: BERT + Heuristique avancée
"""
from typing import List, Optional, Dict, Any
from app.models.schemas import (
    PhishingDetectRequest,
    PhishingDetectResponse,
    ThreatLevel
)
from datetime import datetime
import uuid
import re
from urllib.parse import urlparse
import os
from pathlib import Path

# Import du KeywordScanner
from app.modules.phishing_detect.keyword_scanner import keyword_scanner


class PhishingDetectService:
    """Service de détection de phishing avec IA BERT"""
    
    def __init__(self):
        self.detection_db = {}
        self.classifier = None
        self.model_name = "ealvaradob/bert-finetuned-phishing"
        self._load_model()
    
    def _load_model(self):
        """
        Charge le modèle BERT pour la détection de phishing
        
        Utilise le cache pour ne pas retélécharger à chaque fois
        """
        try:
            from transformers import pipeline
            
            # Définir le répertoire de cache
            cache_dir = Path.home() / ".cache" / "huggingface" / "transformers"
            cache_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"🤖 Chargement du modèle BERT: {self.model_name}")
            print(f"📁 Cache: {cache_dir}")
            
            # Charger le modèle avec cache
            self.classifier = pipeline(
                "text-classification",
                model=self.model_name,
                cache_dir=str(cache_dir),
                device=-1  # CPU (utiliser 0 pour GPU si disponible)
            )
            
            print("✅ Modèle BERT chargé avec succès")
            
        except ImportError:
            print("⚠️ transformers non installé. Installez avec: pip install transformers torch")
            self.classifier = None
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement du modèle BERT: {e}")
            print("💡 Vérifiez votre connexion Internet pour le premier téléchargement")
            self.classifier = None
    
    async def analyze_phishing(self, request: PhishingDetectRequest) -> PhishingDetectResponse:
        """
        Analyse complète avec modèle BERT
        
        Format d'entrée intelligent: concatène sender, subject et body
        """
        detection_id = f"phish_{uuid.uuid4().hex[:8]}"
        
        # Construction du texte complet pour l'analyse IA
        email_text = self._prepare_email_text(request)
        
        # Analyse avec BERT si disponible
        if self.classifier and email_text:
            result = await self._analyze_with_bert(email_text, request)
        else:
            # Fallback heuristique
            result = self._analyze_heuristic(email_text, request)
        
        # Ajouter l'ID et timestamp
        result['detection_id'] = detection_id
        result['timestamp'] = datetime.utcnow()
        
        # Créer la réponse
        response = PhishingDetectResponse(**result)
        
        # Sauvegarder dans la DB (mémoire pour l'instant)
        self.detection_db[detection_id] = response
        
        return response
    
    def _prepare_email_text(self, request: PhishingDetectRequest) -> str:
        """
        Prépare le texte d'email pour l'analyse IA
        
        Format optimisé: Subject: {subject} Sender: {sender} Body: {body}
        """
        parts = []
        
        if request.subject:
            parts.append(f"Subject: {request.subject}")
        
        if request.sender:
            parts.append(f"Sender: {request.sender}")
        
        if request.body:
            # Limiter le body à 1000 caractères pour le modèle
            body_text = request.body[:1000]
            parts.append(f"Body: {body_text}")
        
        return " ".join(parts)
    
    async def _analyze_with_bert(
        self, 
        email_text: str, 
        request: PhishingDetectRequest
    ) -> Dict[str, Any]:
        """
        Analyse HYBRIDE: BERT + KeywordScanner
        
        Score Final = (Score_BERT * 0.6) + (Score_Keywords * 0.4)
        
        Cette approche combine:
        - L'IA (BERT) pour la compréhension contextuelle
        - L'analyse lexicale (Keywords) pour les patterns connus
        """
        try:
            # ============= 1. ANALYSE BERT =============
            print(f"🤖 Analyse BERT...")
            predictions = self.classifier(email_text, truncation=True, max_length=512)
            
            result = predictions[0]
            label = result['label'].upper()
            bert_score = result['score']
            
            # Interpréter le score BERT
            if 'LABEL_1' in label or 'PHISHING' in label:
                bert_confidence = bert_score
            else:
                # LABEL_0 = Safe, donc inverser
                bert_confidence = 1 - bert_score
            
            print(f"   BERT: {bert_confidence:.2%}")
            
            # ============= 2. ANALYSE KEYWORDS =============
            print(f"🔍 Analyse Keywords...")
            # Préparer le texte pour le scanner (sujet + corps uniquement)
            scan_text = ""
            if request.subject:
                scan_text += request.subject + " "
            if request.body:
                scan_text += request.body
            
            keyword_result = keyword_scanner.scan(scan_text)
            keyword_score = keyword_result['score']
            keyword_matches = keyword_result['matches']
            detected_categories = keyword_result['categories']
            
            print(f"   Keywords: {keyword_score:.2%} ({len(keyword_matches)} matches)")
            
            # ============= 3. SCORING HYBRIDE =============
            # Score final = moyenne pondérée
            BERT_WEIGHT = 0.6
            KEYWORD_WEIGHT = 0.4
            
            final_score = (bert_confidence * BERT_WEIGHT) + (keyword_score * KEYWORD_WEIGHT)
            
            print(f"📊 Score Final: {final_score:.2%} = BERT({bert_confidence:.2%}) * 0.6 + Keywords({keyword_score:.2%}) * 0.4")
            
            # ============= 4. DÉTERMINATION DU VERDICT =============
            is_phishing = False
            threat_category = "safe"
            
            if final_score >= 0.8:
                is_phishing = True
                threat_category = "phishing"
            elif final_score >= 0.5:
                is_phishing = True
                threat_category = "suspicious"
            else:
                # Safe, mais vérifier les cas spéciaux
                if keyword_score > 0.7 and bert_confidence < 0.5:
                    # Beaucoup de keywords mais BERT dit safe = Suspicious quand même
                    threat_category = "suspicious"
                    is_phishing = True
                    print(f"⚠️ Override: Keywords élevés ({keyword_score:.2%}) mais BERT bas = SUSPICIOUS")
                else:
                    threat_category = "safe"
            
            # ============= 5. INDICATEURS =============
            indicators = []
            
            # Indicateur BERT
            indicators.append(f"🤖 IA BERT: {bert_confidence:.1%} confiance")
            
            # Indicateur Keywords
            indicators.append(f"🔍 Mots-clés: {keyword_score:.1%} ({len(keyword_matches)} détectés)")
            
            # Score hybride
            indicators.append(f"📊 Score Hybride: {final_score:.1%} = (BERT × 60%) + (Keywords × 40%)")
            
            # Catégories détectées
            if detected_categories:
                cat_names = [keyword_scanner.get_category_name_fr(cat) for cat in detected_categories]
                indicators.append(f"📂 Catégories: {', '.join(cat_names)}")
            
            # Top keywords
            if keyword_matches:
                indicators.append(f"⚠️ Mots suspects: {', '.join(keyword_matches[:5])}")
            
            # Indicateurs complémentaires
            heuristic_indicators = self._get_heuristic_indicators(request)
            indicators.extend(heuristic_indicators)
            
            # URL
            if request.url:
                url_indicators = self._analyze_url_indicators(request.url)
                indicators.extend(url_indicators)
            
            # ============= 6. NIVEAU DE MENACE =============
            threat_level = self._calculate_threat_level(is_phishing, final_score, threat_category)
            
            # ============= 7. RECOMMANDATIONS =============
            recommendations = self._generate_recommendations(
                is_phishing, 
                threat_level, 
                threat_category,
                indicators
            )
            
            return {
                'is_phishing': is_phishing,
                'confidence': final_score,
                'threat_category': threat_category,
                'indicators': indicators if indicators else ["✅ Aucun indicateur suspect détecté"],
                'threat_level': threat_level,
                'recommendations': recommendations,
                'ai_model_used': f"{self.model_name} + KeywordScanner"
            }
            
        except Exception as e:
            print(f"⚠️ Erreur BERT: {e}")
            import traceback
            traceback.print_exc()
            return self._analyze_heuristic(email_text, request)
    
    def _analyze_heuristic(
        self, 
        email_text: str, 
        request: PhishingDetectRequest
    ) -> Dict[str, Any]:
        """
        Analyse heuristique (fallback si BERT non disponible)
        """
        indicators = []
        suspicion_score = 0.0
        
        # Patterns d'urgence
        urgency_patterns = [
            'urgent', 'immediately', 'act now', 'expire', 'suspended',
            'verify now', 'confirm identity', 'unusual activity', 'action required',
            'limited time', 'expires today'
        ]
        
        for pattern in urgency_patterns:
            if pattern in email_text.lower():
                indicators.append(f"⚠️ Langage d'urgence: '{pattern}'")
                suspicion_score += 0.15
        
        # Demandes d'informations sensibles
        sensitive_patterns = [
            'password', 'credit card', 'social security', 'ssn',
            'bank account', 'pin code', 'personal information',
            'confirm your account', 'verify your identity'
        ]
        
        for pattern in sensitive_patterns:
            if pattern in email_text.lower():
                indicators.append(f"🔴 Demande d'info sensible: '{pattern}'")
                suspicion_score += 0.25
        
        # Menaces
        threat_patterns = [
            'legal action', 'police', 'arrest', 'lawsuit', 'close account',
            'suspended', 'blocked', 'terminated'
        ]
        
        for pattern in threat_patterns:
            if pattern in email_text.lower():
                indicators.append(f"⚠️ Langage menaçant: '{pattern}'")
                suspicion_score += 0.2
        
        # Analyse de l'expéditeur
        if request.sender:
            sender_indicators = self._analyze_sender(request.sender)
            indicators.extend(sender_indicators)
            if sender_indicators:
                suspicion_score += 0.2 * len(sender_indicators)
        
        # Analyse URL si fournie
        if request.url:
            url_indicators = self._analyze_url_indicators(request.url)
            indicators.extend(url_indicators)
            if url_indicators:
                suspicion_score += 0.3 * len(url_indicators)
        
        confidence = min(suspicion_score, 0.99)
        is_phishing = suspicion_score > 0.5
        
        # Catégoriser
        if confidence < 0.5:
            threat_category = "safe"
        elif confidence < 0.8:
            threat_category = "suspicious"
        else:
            threat_category = "phishing"
        
        threat_level = self._calculate_threat_level(is_phishing, confidence, threat_category)
        
        recommendations = self._generate_recommendations(
            is_phishing,
            threat_level,
            threat_category,
            indicators
        )
        
        if not indicators:
            indicators = ["✅ Aucun indicateur suspect majeur détecté"]
        
        return {
            'is_phishing': is_phishing,
            'confidence': confidence,
            'threat_category': threat_category,
            'indicators': indicators,
            'threat_level': threat_level,
            'recommendations': recommendations,
            'ai_model_used': 'Heuristic (fallback)'
        }
    
    def _get_heuristic_indicators(self, request: PhishingDetectRequest) -> List[str]:
        """Récupère des indicateurs heuristiques complémentaires"""
        indicators = []
        
        # Analyser l'expéditeur
        if request.sender:
            sender_indicators = self._analyze_sender(request.sender)
            indicators.extend(sender_indicators)
        
        # Analyser le sujet
        if request.subject:
            subject_lower = request.subject.lower()
            
            if any(word in subject_lower for word in ['urgent', 'action required', 'verify', 'suspended']):
                indicators.append("⚠️ Sujet contient des mots d'urgence")
            
            if request.subject.isupper():
                indicators.append("⚠️ Sujet en majuscules (tactique d'urgence)")
        
        return indicators
    
    def _analyze_sender(self, sender: str) -> List[str]:
        """Analyse l'adresse email de l'expéditeur"""
        indicators = []
        
        try:
            # Extraire le domaine
            if '@' in sender:
                domain = sender.split('@')[1].lower()
                
                # Domaines suspects
                suspicious_domains = [
                    'temp', 'fake', 'secure', 'verify', 'account',
                    'alert', 'support-', '-support', 'login'
                ]
                
                if any(susp in domain for susp in suspicious_domains):
                    indicators.append(f"🔴 Domaine suspect: {domain}")
                
                # TLD suspects
                suspicious_tlds = ['.xyz', '.top', '.club', '.online', '.site']
                if any(domain.endswith(tld) for tld in suspicious_tlds):
                    indicators.append(f"⚠️ Extension de domaine suspecte")
                
                # Beaucoup de chiffres dans le domaine
                digit_count = sum(c.isdigit() for c in domain)
                if digit_count > 3:
                    indicators.append(f"⚠️ Trop de chiffres dans le domaine ({digit_count})")
        
        except Exception as e:
            pass
        
        return indicators
    
    def _analyze_url_indicators(self, url: str) -> List[str]:
        """Analyse une URL pour des indicateurs suspects"""
        indicators = []
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # IP au lieu de domaine
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
                indicators.append("🔴 URL utilise une adresse IP (très suspect)")
            
            # Mots-clés dans l'URL
            suspicious_keywords = [
                'login', 'verify', 'secure', 'account', 'update',
                'confirm', 'suspended', 'paypal', 'banking'
            ]
            
            found = [kw for kw in suspicious_keywords if kw in url.lower()]
            if found:
                indicators.append(f"⚠️ Mots-clés suspects dans URL: {', '.join(found[:3])}")
            
            # Typosquatting
            typo_targets = {
                'g00gle': 'google',
                'paypa1': 'paypal',
                'micros0ft': 'microsoft',
                'app1e': 'apple',
                'faceb00k': 'facebook',
                'amaz0n': 'amazon'
            }
            
            for typo, real in typo_targets.items():
                if typo in domain:
                    indicators.append(f"🔴 Typosquatting possible de '{real}'")
        
        except Exception:
            pass
        
        return indicators
    
    def _calculate_threat_level(
        self,
        is_phishing: bool,
        confidence: float,
        threat_category: str
    ) -> ThreatLevel:
        """Calcule le niveau de menace"""
        
        if not is_phishing or threat_category == "safe":
            return ThreatLevel.LOW
        
        if threat_category == "phishing" and confidence > 0.8:
            return ThreatLevel.CRITICAL
        elif threat_category == "phishing":
            return ThreatLevel.HIGH
        elif threat_category == "suspicious":
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def _generate_recommendations(
        self,
        is_phishing: bool,
        threat_level: ThreatLevel,
        threat_category: str,
        indicators: List[str]
    ) -> List[str]:
        """Génère des recommandations personnalisées"""
        recommendations = []
        
        if threat_category == "phishing":
            recommendations.extend([
                "🚫 NE CLIQUEZ PAS sur les liens de ce message",
                "🚫 NE FOURNISSEZ AUCUNE information personnelle",
                "🗑️ Supprimez ce message immédiatement",
                "📧 Contactez l'organisation par ses canaux officiels",
                "⚠️ Signalez ce phishing à votre service IT/sécurité"
            ])
        elif threat_category == "suspicious":
            recommendations.extend([
                "⚠️ Soyez très prudent avec ce message",
                "🔍 Vérifiez l'identité de l'expéditeur",
                "🔗 N'ouvrez pas les liens sans vérification",
                "📞 Contactez l'expéditeur par un canal alternatif",
                "🤔 En cas de doute, ne répondez pas"
            ])
        else:
            recommendations.extend([
                "✅ Ce message semble légitime",
                "👀 Vérifiez quand même l'expéditeur pour être sûr",
                "🔗 Survolez les liens avant de cliquer",
                "🔐 N'entrez jamais vos mots de passe si demandé"
            ])
        
        return recommendations
    
    async def get_history(self, limit: int = 10) -> List[PhishingDetectResponse]:
        """Récupère l'historique des détections"""
        return list(self.detection_db.values())[:limit]
    
    async def get_detection(self, detection_id: str) -> Optional[PhishingDetectResponse]:
        """Récupère une détection spécifique"""
        return self.detection_db.get(detection_id)
