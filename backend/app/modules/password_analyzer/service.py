"""
Service pour le module Password Analyzer
Analyse de force des mots de passe avec zxcvbn
"""
from zxcvbn import zxcvbn
from datetime import datetime
from app.models.schemas import PasswordAnalyzeResponse


class PasswordAnalyzerService:
    """Service d'analyse de mots de passe"""
    
    def __init__(self):
        self.strength_levels = {
            0: "very_weak",
            1: "weak",
            2: "fair",
            3: "strong",
            4: "very_strong"
        }
        
        # Dictionnaire de traduction COMPLET (Anglais -> Français)
        self.translations = {
            # Suggestions courantes de zxcvbn
            "Use a few words, avoid common phrases": "Utilisez une phrase secrète, évitez les expressions courantes",
            "No need for symbols, digits, or uppercase letters": "Pas besoin de symboles si vous utilisez une longue phrase",
            "Add another word or two. Uncommon words are better.": "Ajoutez un ou deux mots de plus. Les mots rares sont meilleurs.",
            "Capitalization doesn't help very much": "Les majuscules n'aident pas beaucoup",
            "All-uppercase is almost as easy to guess as all-lowercase": "Tout en majuscules est aussi facile à deviner que tout en minuscules",
            "Reversed words aren't much harder to guess": "Les mots inversés ne sont pas plus difficiles à deviner",
            "Predictable substitutions like '@' instead of 'a' don't help very much": "Les substitutions prévisibles comme '@' au lieu de 'a' n'aident pas beaucoup",
            "Use a longer keyboard pattern with more turns": "Utilisez un motif de clavier plus long",
            "Avoid repeated words and characters": "Évitez les mots et caractères répétés",
            "Avoid sequences": "Évitez les séquences (abc, 123)",
            "Avoid recent years": "Évitez les années récentes",
            "Avoid years that are associated with you": "Évitez les années associées à vous",
            "Avoid dates and years that are associated with you": "Évitez les dates qui vous concernent",
            "This is a top-10 common password": "C'est un mot de passe dans le top 10 des plus courants",
            "This is a top-100 common password": "C'est un mot de passe dans le top 100 des plus courants",
            "This is a very common password": "C'est un mot de passe très courant",
            "This is similar to a commonly used password": "C'est similaire à un mot de passe couramment utilisé",
            "A word by itself is easy to guess": "Un mot seul est facile à deviner",
            "Names and surnames by themselves are easy to guess": "Les noms et prénoms seuls sont faciles à deviner",
            "Common names and surnames are easy to guess": "Les noms et prénoms courants sont faciles à deviner",
            "Straight rows of keys are easy to guess": "Les lignes de touches sont faciles à deviner",
            "Short keyboard patterns are easy to guess": "Les motifs courts de clavier sont faciles à deviner",
            "Sequences like abc or 6543 are easy to guess": "Les séquences comme abc ou 6543 sont faciles à deviner",
            "Recent years are easy to guess": "Les années récentes sont faciles à deviner",
            "Dates are often easy to guess": "Les dates sont souvent faciles à deviner",
        }
    
    async def analyze_password(self, password: str) -> PasswordAnalyzeResponse:
        """
        Analyse un mot de passe avec zxcvbn
        
        Args:
            password: Le mot de passe à analyser (non-vide, déjà validé)
            
        Returns:
            PasswordAnalyzeResponse avec toutes les métriques
        """
        try:
            print(f"🔍 Analyzing password (length: {len(password)})...")
            
            # 1. Analyse avec zxcvbn
            result = zxcvbn(password)
            print(f"   zxcvbn analysis done")
            
            # 2. Extraction sécurisée
            score = result.get('score', 0)
            crack_time_seconds = result.get('crack_times_seconds', {}).get('offline_slow_hashing_1e4_per_second', 0)
            
            # 3. Formater le temps de crackage en FRANÇAIS
            crack_time_display = self._format_crack_time_french(crack_time_seconds)
            
            # 4. Calcul de l'entropie
            entropy = result.get('guesses_log10', 0) * 3.32  # log10 to bits
            
            # 5. Générer les suggestions (traduites)
            suggestions = self._generate_suggestions(result, password)
            
            # 6. Warning si faible
            warning = None
            if score <= 1:
                warning = "⚠️ Ce mot de passe est très faible et peut être cracké rapidement"
            elif score == 2:
                warning = "Ce mot de passe est moyen. Ajoutez plus de complexité"
            
            # 7. Traduire le warning de zxcvbn
            warning_message = result.get('feedback', {}).get('warning', '')
            translated_warning = self._translate(warning_message) if warning_message else ''
            
            print(f"   Score: {score}/4, Time: {crack_time_display}")
            
            # 8. Construire la réponse
            return PasswordAnalyzeResponse(
                score=score,
                strength=self.strength_levels.get(score, "unknown"),
                crack_time_seconds=crack_time_seconds,
                crack_time_display=crack_time_display,
                entropy=entropy,
                suggestions=suggestions,
                warning=warning,
                feedback={
                    "warning_message": translated_warning,
                    "suggestions_raw": result.get('feedback', {}).get('suggestions', []),
                    "pattern_matches": len(result.get('sequence', [])),
                    "guesses": result.get('guesses', 0)
                },
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            print(f"❌ ERROR in service: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            raise ValueError(f"Erreur lors de l'analyse: {str(e)}")
    
    def _translate(self, text: str) -> str:
        """Traduit un texte anglais en français"""
        return self.translations.get(text, text)
    
    def _format_crack_time_french(self, seconds: float) -> str:
        """
        Formate le temps de crackage en FRANÇAIS et LISIBLE
        
        Exemples:
        - "Instantané"
        - "3 secondes"
        - "5 minutes"
        - "2 heures"
        - "15 jours"
        - "3 ans"
        - "400 siècles"
        """
        if seconds < 0.001:
            return "Instantané"
        elif seconds < 1:
            return "Moins d'une seconde"
        elif seconds < 60:
            s = int(seconds)
            return f"{s} seconde{'s' if s > 1 else ''}"
        elif seconds < 3600:
            m = int(seconds / 60)
            return f"{m} minute{'s' if m > 1 else ''}"
        elif seconds < 86400:
            h = int(seconds / 3600)
            return f"{h} heure{'s' if h > 1 else ''}"
        elif seconds < 2592000:  # 30 jours
            d = int(seconds / 86400)
            return f"{d} jour{'s' if d > 1 else ''}"
        elif seconds < 31536000:  # 1 an
            mo = int(seconds / 2592000)
            return f"{mo} mois"
        elif seconds < 3153600000:  # 100 ans
            y = int(seconds / 31536000)
            return f"{y} an{'s' if y > 1 else ''}"
        else:
            c = int(seconds / 3153600000)
            return f"{c} siècle{'s' if c > 1 else ''}"
    
    def _generate_suggestions(self, zxcvbn_result: dict, password: str) -> list[str]:
        """Génère des suggestions personnalisées d'amélioration (traduites)"""
        suggestions = []
        
        # 1. Suggestions de base de zxcvbn (traduites)
        base_suggestions = zxcvbn_result.get('feedback', {}).get('suggestions', [])
        for suggestion in base_suggestions:
            translated = self._translate(suggestion)
            suggestions.append(translated)
        
        # 2. Suggestions personnalisées
        if len(password) < 12:
            suggestions.append("✓ Utilisez au moins 12 caractères")
        
        if not any(c.isupper() for c in password):
            suggestions.append("✓ Ajoutez des lettres majuscules (A-Z)")
        
        if not any(c.islower() for c in password):
            suggestions.append("✓ Ajoutez des lettres minuscules (a-z)")
        
        if not any(c.isdigit() for c in password):
            suggestions.append("✓ Ajoutez des chiffres (0-9)")
        
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            suggestions.append("✓ Ajoutez des symboles spéciaux (!@#$%^&*)")
        
        # 3. Limiter à 5 suggestions max (dédupliquées)
        unique_suggestions = []
        seen = set()
        for sugg in suggestions:
            if sugg not in seen:
                unique_suggestions.append(sugg)
                seen.add(sugg)
        
        return unique_suggestions[:5]
