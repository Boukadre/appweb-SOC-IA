"""
KeywordScanner pour détection heuristique de phishing
Analyse lexicale avancée avec catégories de mots-clés
"""
from typing import Dict, List, Tuple
import re


class KeywordScanner:
    """Scanner de mots-clés pour détection de phishing par analyse lexicale"""
    
    def __init__(self):
        # Dictionnaire de mots-clés par catégorie (en minuscules)
        self.keywords = {
            "promesses_exagerees": [
                "gratuit", "100% gratuit", "remboursé", "cadeau", "appel gratuit",
                "pas de frais", "inscription gratuite", "essai gratuit", "gratuitement",
                "réduction", "rabais", "meilleur prix", "promotion", "offre spéciale",
                "comparer les prix", "pour seulement", "pas cher", "abordable",
                "coupon", "50%", "promo", "soldes", "moins cher"
            ],
            "urgence_pression": [
                "faites vite", "urgent", "profitez maintenant", "offre limitée",
                "dès maintenant", "dès aujourd'hui", "n'hésitez plus", "appelez maintenant",
                "expire", "temps limité", "durée limitée", "quantités limitées",
                "rupture de stock", "dernière chance", "ne ratez pas", "agissez maintenant",
                "immédiatement", "aujourd'hui seulement", "vite", "rapide"
            ],
            "gain_suspect": [
                "vous avez gagné", "bravo", "ouvrez pour découvrir", "cadeau exceptionnel",
                "gagnant", "sélectionné", "félicitations", "récompense", "pour vous seulement",
                "garanti", "100% sûr", "certifié", "sans risque", "deal incroyable",
                "bonus", "bonne affaire", "vu à la tv", "satisfaction garantie",
                "pas d'arnaque", "aucun risque", "miracle", "incroyable", "exceptionnel"
            ],
            "vocabulaire_financier": [
                "cash", "money", "argent facile", "argent rapide", "gagner de l'argent",
                "revenu supplémentaire", "bénéfice", "millions", "economiser", "euros",
                "profits", "gains", "votre propre patron", "carte de crédit",
                "carte bancaire", "investissement", "faillite", "revenu", "salaire",
                "taux d'intérêt", "sortir des dettes", "remboursement intégral",
                "chèque", "virement bancaire", "paypal", "rendement", "placer votre argent",
                "bitcoin", "crypto", "dollars"
            ],
            "marketing_agressif": [
                "ventes", "soldes", "augmentez vos ventes", "cliquez ici", "commande",
                "chiffre d'affaires", "marketing", "acheter", "augmentez", "acheter maintenant",
                "commandez", "inscrivez-vous", "téléchargez", "remplissez",  "achetez",
                "réservez", "souscrivez"
            ]
        }
        
        # Poids par catégorie (pour le scoring)
        self.category_weights = {
            "promesses_exagerees": 0.15,
            "urgence_pression": 0.25,
            "gain_suspect": 0.30,
            "vocabulaire_financier": 0.35,
            "marketing_agressif": 0.20
        }
    
    def scan(self, text: str) -> Dict[str, any]:
        """
        Scanne un texte pour détecter des mots-clés suspects
        
        Args:
            text: Texte à analyser (sujet + corps email)
            
        Returns:
            Dict contenant:
            - score: Score heuristique (0.0 à 1.0)
            - matches: Liste des mots-clés trouvés
            - categories: Catégories détectées avec leurs scores
            - density: Densité de mots-clés (matches / total_words)
        """
        # Normaliser le texte
        text_lower = text.lower()
        
        # Résultats par catégorie
        category_matches = {}
        all_matches = []
        category_scores = {}
        
        # Scanner chaque catégorie
        for category, keywords in self.keywords.items():
            matches = []
            
            for keyword in keywords:
                # Recherche de mot entier ou expression
                if self._keyword_present(keyword, text_lower):
                    matches.append(keyword)
                    all_matches.append(keyword)
            
            category_matches[category] = matches
            
            # Calculer le score de la catégorie
            if matches:
                # Score = (nombre de matches / total keywords catégorie) * poids
                match_ratio = len(matches) / len(keywords)
                category_scores[category] = match_ratio * self.category_weights[category]
            else:
                category_scores[category] = 0.0
        
        # Score heuristique total (somme pondérée)
        heuristic_score = sum(category_scores.values())
        
        # Limiter entre 0 et 1
        heuristic_score = min(heuristic_score, 1.0)
        
        # Calculer la densité (mots-clés / total mots)
        total_words = len(text.split())
        density = len(all_matches) / total_words if total_words > 0 else 0
        
        # Bonus si haute densité
        if density > 0.1:  # Plus de 10% du texte = mots-clés
            heuristic_score = min(heuristic_score * 1.2, 1.0)
        
        # Catégories détectées (non vides)
        detected_categories = [
            cat for cat, matches in category_matches.items() if matches
        ]
        
        return {
            "score": heuristic_score,
            "matches": all_matches[:15],  # Limiter à 15 matches pour lisibilité
            "categories": detected_categories,
            "category_scores": category_scores,
            "density": density,
            "total_matches": len(all_matches)
        }
    
    def _keyword_present(self, keyword: str, text: str) -> bool:
        """
        Vérifie si un mot-clé est présent dans le texte
        
        Utilise une recherche de mot entier pour éviter les faux positifs
        (ex: "gratuit" ne match pas "gratuitement" si ce n'est pas voulu)
        """
        # Pour les expressions (plusieurs mots)
        if " " in keyword:
            return keyword in text
        
        # Pour les mots simples, utiliser word boundaries
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return bool(re.search(pattern, text))
    
    def get_category_name_fr(self, category: str) -> str:
        """Retourne le nom français d'une catégorie"""
        names = {
            "promesses_exagerees": "Promesses Exagérées",
            "urgence_pression": "Urgence & Pression",
            "gain_suspect": "Gain Suspect",
            "vocabulaire_financier": "Vocabulaire Financier",
            "marketing_agressif": "Marketing Agressif"
        }
        return names.get(category, category)


# Instance singleton
keyword_scanner = KeywordScanner()

