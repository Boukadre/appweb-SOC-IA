# 🛡️ Cyber IA Platform

Plateforme professionnelle d'analyse de sécurité cyber avec Intelligence Artificielle.

## 🏗️ Architecture

Ce projet utilise une architecture **monorepo découplée** avec :

- **Backend** : FastAPI (Python) - API REST avec 4 modules d'IA
- **Frontend** : Next.js 14+ (TypeScript) - Interface utilisateur professionnelle

---

## 📁 Structure du Projet

```
Projet-cyber-IA-2/
├── backend/           # API FastAPI
│   ├── app/
│   │   ├── main.py           # Point d'entrée
│   │   ├── core/             # Configuration globale
│   │   ├── models/           # Modèles Pydantic
│   │   └── modules/          # 4 modules IA
│   │       ├── network_scan/
│   │       ├── malware_analysis/
│   │       ├── phishing_detect/
│   │       └── report_gen/
│   └── requirements.txt
│
└── frontend/          # Interface Next.js
    ├── src/
    │   ├── app/              # Pages (App Router)
    │   ├── components/       # Composants UI
    │   ├── lib/              # Utilitaires
    │   └── services/         # Client API
    └── package.json
```

---

## 🚀 Démarrage Rapide

### Backend (FastAPI)

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : **http://localhost:8000**
Documentation interactive : **http://localhost:8000/api/docs**

### Frontend (Next.js)

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

L'interface sera accessible sur : **http://localhost:3000**

---

## 🎨 Design System

### Thème "Cyber-Security Dashboard"

- **Mode sombre par défaut** avec fond `#0a0e1a`
- **Couleurs principales** :
  - Cyan électrique : `#00f0ff`
  - Bleu profond : `#0066ff`
  - Magenta : `#ff00ff`
- **Polices** : Inter (texte) + JetBrains Mono (code)
- **Effets** : Bordures lumineuses, animations subtiles, grid background

---

## 📡 Modules IA

### 1. Network Scan
Analyse réseau et détection de vulnérabilités
- Endpoint : `/api/network-scan`
- Fonctionnalités : Scan de ports, détection de services, scoring de menaces

### 2. Malware Analysis
Analyse de fichiers suspects
- Endpoint : `/api/malware-analysis`
- Fonctionnalités : Upload de fichiers, analyse statique/dynamique, classification IA

### 3. Phishing Detection
Détection de phishing dans emails et URLs
- Endpoint : `/api/phishing-detect`
- Fonctionnalités : Analyse d'URL, détection de patterns malveillants, NLP

### 4. Report Generation
Génération de rapports consolidés
- Endpoint : `/api/report-gen`
- Fonctionnalités : Export PDF/HTML/JSON, statistiques, recommandations

---

## 🛠️ Technologies

### Backend
- **FastAPI** : Framework web moderne et performant
- **Pydantic** : Validation de données
- **Python-Jose** : JWT pour l'authentification
- **Uvicorn** : Serveur ASGI

### Frontend
- **Next.js 14+** : Framework React avec App Router
- **TypeScript** : Typage statique
- **Tailwind CSS** : Framework CSS utility-first
- **Radix UI** : Composants accessibles
- **Lucide React** : Icônes modernes
- **Axios** : Client HTTP

---

## 📋 TODO - Prochaines Étapes

### Backend
- [ ] Implémenter la logique IA pour chaque module
- [ ] Intégrer avec des APIs externes (VirusTotal, Shodan)
- [ ] Ajouter authentification JWT complète
- [ ] Configurer une base de données (PostgreSQL)
- [ ] Implémenter le rate limiting
- [ ] Ajouter des tests unitaires (pytest)

### Frontend
- [ ] Connecter les pages aux endpoints API
- [ ] Implémenter la gestion d'état (Context API ou Zustand)
- [ ] Ajouter des graphiques (Recharts)
- [ ] Implémenter le système de notifications
- [ ] Ajouter l'authentification côté client
- [ ] Mode responsive pour mobile

---

## 🔐 Sécurité

- CORS configuré pour autoriser uniquement le frontend
- Variables d'environnement pour les secrets (`.env`)
- Validation des données avec Pydantic
- Authentification JWT (à activer)

---

## 📝 Licence

Projet privé - Tous droits réservés

---

## 👨‍💻 Développement

**Architecture conçue pour la scalabilité et la maintenabilité.**

Pour toute question ou contribution, consultez la documentation dans chaque module.

