# 🚀 Guide de Démarrage Rapide - Cyber IA Platform

## 📋 Prérequis

- **Python 3.9+** installé
- **Node.js 18+** et npm installés
- **Git** (optionnel)

---

## ⚡ Installation et Lancement (5 minutes)

### 1️⃣ Backend (FastAPI) - Terminal 1

```powershell
# Aller dans le dossier backend
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ **API accessible sur** : http://localhost:8000  
📖 **Documentation interactive** : http://localhost:8000/api/docs

---

### 2️⃣ Frontend (Next.js) - Terminal 2

```powershell
# Aller dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

✅ **Application accessible sur** : http://localhost:3000

---

## 🎯 Modules Disponibles

### 1. **Network Scan** (`/network-scan`)
- Scanne des adresses IP ou domaines
- Détecte les ports ouverts
- Identifie les vulnérabilités réseau

**Test rapide** :
- Cible : `scanme.nmap.org` ou `example.com`

---

### 2. **CVE Scanner** (`/cve-scanner`) 🆕
- Détecte les technologies web (WordPress, serveurs, frameworks)
- Identifie les CVE associées
- Évalue le niveau de risque global

**Test rapide** :
- URL : `https://wordpress.org`
- URL : `https://httpbin.org`

**Technologies détectées** :
- CMS (WordPress, Joomla, Drupal)
- Serveurs web (Apache, nginx)
- Langages (PHP, Python)
- Frameworks JavaScript

---

### 3. **Malware Analysis** (`/malware-analysis`)
- Upload de fichiers suspects
- Analyse heuristique
- Score de confiance

**Test rapide** :
- Nom de fichier : `suspicious_file.exe`
- Nom de fichier : `document.pdf`

---

### 4. **Phishing Detection** (`/phishing-detect`)
- **Analyse d'URL** avec détection de patterns
- **Analyse d'email** avec IA (Hugging Face)
- Détection de mots-clés suspects
- Score de confiance IA

**Tests rapides** :

**URLs suspectes** :
```
https://paypa1-secure-login.com
http://192.168.1.1/admin
https://bit.ly/suspicious
```

**URLs légitimes** :
```
https://google.com
https://github.com
```

**Email phishing typique** :
```
URGENT: Your account will be suspended!

Dear user,

We detected unusual activity on your account. 
Please verify your identity immediately by clicking 
the link below and entering your password:

http://verify-account-now.suspicious.com

If you don't act within 24 hours, your account 
will be permanently closed.

Best regards,
Security Team
```

---

### 5. **Password Analyzer** (`/password-analyzer`) 🆕
- Analyse en temps réel
- Score de force (0-4)
- Temps de crackage estimé
- Entropie calculée
- Suggestions personnalisées

**Tests rapides** :

**Très faible** : `password` ou `123456`  
**Faible** : `Password1`  
**Moyen** : `MyP@ssw0rd`  
**Fort** : `Tr0ub4dor&3`  
**Très fort** : `correct-horse-battery-staple-2024!`

---

### 6. **Report Generation** (`/report-gen`)
- Génération de rapports consolidés
- Formats : PDF, HTML, JSON

---

## 🧪 Tester l'API directement

Accédez à la documentation interactive Swagger :
👉 http://localhost:8000/api/docs

Vous pouvez tester tous les endpoints directement depuis cette interface.

---

## 🔧 Configuration

### Variables d'environnement Backend

Créez un fichier `.env` dans `backend/` :

```env
APP_NAME="Cyber IA Platform"
ENVIRONMENT=development
DEBUG=True

SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256

ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

DATABASE_URL=sqlite:///./cyber_ia.db

MODEL_PATH=./models
MAX_FILE_SIZE_MB=50
```

### Variables d'environnement Frontend

Créez un fichier `.env.local` dans `frontend/` :

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Cyber IA Platform
```

---

## 📦 Dépendances IA

Le projet utilise plusieurs librairies IA :

### Backend
- **transformers** + **torch** : Détection phishing avec Hugging Face
- **zxcvbn-python** : Analyse de force des mots de passe
- **builtwith** : Détection de technologies web
- **beautifulsoup4** : Parsing HTML pour CVE scan

### Installation optionnelle (pour GPU)

Si vous avez un GPU NVIDIA :

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 🐛 Dépannage

### Erreur : "Port 8000 déjà utilisé"

```bash
# Trouver le processus
netstat -ano | findstr :8000

# Tuer le processus (remplacer PID)
taskkill /PID <PID> /F
```

### Erreur : "Module not found"

```bash
# Backend
pip install -r requirements.txt --upgrade

# Frontend
npm install
```

### Erreur CORS

Vérifiez que `ALLOWED_ORIGINS` dans `.env` contient l'URL du frontend.

---

## 🎨 Architecture Technique

### Backend (FastAPI)
- **Architecture modulaire** : Chaque module (CVE, Password, etc.) est indépendant
- **Validation Pydantic** : Toutes les entrées/sorties sont validées
- **Async/Await** : Performances optimales
- **Documentation auto-générée** : Swagger UI intégré

### Frontend (Next.js 14)
- **App Router** : Routing moderne
- **TypeScript** : Typage complet
- **Tailwind CSS** : Styling utility-first
- **API Client** : Axios avec intercepteurs

---

## 📊 État des Modules

| Module | Backend | Frontend | IA | Status |
|--------|---------|----------|----|---------| 
| Network Scan | ✅ | ✅ | ⚠️ Mock | Fonctionnel |
| CVE Scanner | ✅ | ✅ | ✅ builtwith | **Fonctionnel** |
| Malware Analysis | ✅ | ✅ | ⚠️ Mock | Fonctionnel |
| Phishing Detection | ✅ | ✅ | ✅ Hugging Face | **Fonctionnel** |
| Password Analyzer | ✅ | ✅ | ✅ zxcvbn | **Fonctionnel** |
| Report Gen | ✅ | ✅ | ⚠️ Mock | Fonctionnel |

---

## 🚀 Prochaines Améliorations

### Backend
- [ ] Implémenter Nmap pour Network Scan réel
- [ ] Intégrer VirusTotal API pour Malware Analysis
- [ ] Ajouter une base de données PostgreSQL
- [ ] Implémenter l'authentification JWT complète
- [ ] Ajouter rate limiting Redis

### Frontend
- [ ] Ajouter des graphiques (Recharts)
- [ ] Implémenter le système de notifications
- [ ] Ajouter pagination dans l'historique
- [ ] Mode responsive mobile optimisé
- [ ] Thème clair/sombre switchable

### IA
- [ ] Fine-tuner un modèle de détection phishing spécifique
- [ ] Ajouter un modèle de classification malware
- [ ] Intégrer GPT pour génération de rapports

---

## 📝 Licence

Projet privé - Tous droits réservés

---

## 🆘 Support

En cas de problème :
1. Vérifiez que Python 3.9+ et Node.js 18+ sont installés
2. Vérifiez que les ports 8000 et 3000 sont libres
3. Consultez les logs dans les terminaux

**Bon hacking éthique !** 🛡️🔐



