# 🔑 CONFIGURATION DES CLÉS API

Ce fichier explique comment configurer vos clés API pour la plateforme Cyber IA.

---

## 📋 FICHIER .env À CRÉER

Créez un fichier `backend/.env` avec le contenu suivant :

```bash
# ============================================
# CYBER IA PLATFORM - CONFIGURATION
# ============================================

# ============================================
# Application Configuration
# ============================================
APP_NAME="Cyber IA Platform"
ENVIRONMENT=development
DEBUG=True

# ============================================
# Security
# ============================================
SECRET_KEY=your-secret-key-change-in-production-please-use-strong-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================
# Database
# ============================================
DATABASE_URL=sqlite:///./cyber_ia.db

# ============================================
# EXTERNAL APIs - CLÉS SECRÈTES
# ============================================
# ⚠️ NE JAMAIS COMMIT CES CLÉS DANS GIT

# AbuseIPDB (Network Scan - Réputation IP)
# Obtenez votre clé gratuite: https://www.abuseipdb.com/api
ABUSEIPDB_API_KEY=votre_cle_abuseipdb_ici
ABUSEIPDB_BASE_URL=https://api.abuseipdb.com/api/v2

# VirusTotal (Malware Analysis)
# Obtenez votre clé gratuite: https://www.virustotal.com/gui/join-us
VIRUSTOTAL_API_KEY=votre_cle_virustotal_ici
VIRUSTOTAL_BASE_URL=https://www.virustotal.com/api/v3

# Shodan (Optionnel - Pour scan réseau avancé)
# Obtenez votre clé: https://account.shodan.io/register
SHODAN_API_KEY=votre_cle_shodan_ici

# ============================================
# AI Models Configuration
# ============================================
AI_MODEL_PATH=./models
HF_PHISHING_MODEL=ealvaradob/bert-finetuned-phishing
MODEL_LOADING_STRATEGY=startup
AI_DEVICE=cpu

# ============================================
# Performance & Limits
# ============================================
MAX_FILE_SIZE_MB=100
RATE_LIMIT_PER_MINUTE=60
EXTERNAL_API_TIMEOUT=30
LOG_LEVEL=INFO

# ============================================
# CORS (Frontend URLs autorisées)
# ============================================
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 🔑 COMMENT OBTENIR LES CLÉS API

### 1. AbuseIPDB (Gratuit)

**Utilité :** Analyse de réputation des adresses IP

**Étapes :**
1. Créer un compte : https://www.abuseipdb.com/api
2. Vérifier votre email
3. Aller dans "API" → "Generate API Key"
4. Copier la clé dans `.env` : `ABUSEIPDB_API_KEY=votre_cle`

**Limites gratuites :**
- 1000 requêtes/jour
- Largement suffisant pour un usage normal

---

### 2. VirusTotal (Gratuit)

**Utilité :** Analyse de fichiers suspects (70+ moteurs antivirus)

**Étapes :**
1. Créer un compte : https://www.virustotal.com/gui/join-us
2. Aller dans votre profil → "API Key"
3. Copier la clé dans `.env` : `VIRUSTOTAL_API_KEY=votre_cle`

**Limites gratuites :**
- 4 requêtes/minute
- 500 requêtes/jour
- Suffisant pour tester et usage modéré

---

### 3. Shodan (Optionnel)

**Utilité :** Scan réseau avancé (recherche d'appareils IoT, etc.)

**Étapes :**
1. Créer un compte : https://account.shodan.io/register
2. Aller dans "Account" → "API Key"
3. Copier la clé dans `.env` : `SHODAN_API_KEY=votre_cle`

**⚠️ Note :** Shodan est optionnel, la plateforme fonctionne sans

---

## 📝 INSTRUCTIONS DE CONFIGURATION

### Méthode 1 : Copie rapide

```bash
# À la racine du projet
cd backend
cp API_KEYS_SETUP.md .env
# Puis éditez .env avec vos vraies clés
```

### Méthode 2 : Création manuelle

```bash
cd backend
nano .env
# ou
notepad .env
```

Puis collez le contenu ci-dessus et remplacez les valeurs.

---

## ✅ VÉRIFICATION

Après configuration, démarrez le backend :

```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Vous devriez voir :**

```
✅ Toutes les clés API sont configurées
```

**Ou si des clés manquent :**

```
⚠️  AVERTISSEMENT - Configuration API
⚠️  VIRUSTOTAL_API_KEY non configurée - Malware Analysis limité
⚠️  ABUSEIPDB_API_KEY non configurée - Network Scan limité
```

---

## 🔒 SÉCURITÉ

### ✅ BONNES PRATIQUES

- ✅ Le fichier `.env` est **ignoré par Git** (voir `.gitignore`)
- ✅ Ne partagez **JAMAIS** vos clés API
- ✅ Utilisez des clés différentes pour dev/prod
- ✅ Régénérez les clés si elles sont exposées
- ✅ Limitez les permissions des clés API

### ❌ NE JAMAIS

- ❌ Commiter le `.env` dans Git
- ❌ Partager vos clés dans Slack/Discord
- ❌ Hardcoder les clés dans le code
- ❌ Utiliser les mêmes clés en production

---

## 🆘 DÉPANNAGE

### Le backend ne trouve pas le .env

**Solution :** Assurez-vous que `.env` est dans `backend/.env`

```bash
backend/
  .env          ← ICI
  app/
  requirements.txt
```

### Les clés ne sont pas chargées

**Vérifications :**
1. Le fichier s'appelle exactement `.env` (pas `.env.txt`)
2. Les variables n'ont pas d'espaces : `KEY=value` (pas `KEY = value`)
3. Pas de guillemets inutiles : `KEY=abc123` (pas `KEY="abc123"`)

### Test manuel des clés

```bash
# Dans le terminal Python
cd backend
python

>>> from app.core.config import settings
>>> print(settings.VIRUSTOTAL_API_KEY)
>>> print(settings.ABUSEIPDB_API_KEY)
```

---

## 📚 RESSOURCES

- **AbuseIPDB Docs :** https://docs.abuseipdb.com/
- **VirusTotal Docs :** https://developers.virustotal.com/
- **Pydantic Settings :** https://docs.pydantic.dev/latest/concepts/pydantic_settings/

---

**🔑 Configuration terminée ! Vous pouvez maintenant utiliser toutes les fonctionnalités de la plateforme.**

