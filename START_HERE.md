# 🚀 START HERE - Quick Setup Guide

## ⚡ Installation Ultra-Rapide (5 minutes)

### Étape 1 : Créer le fichier .env

**C'EST L'ÉTAPE LA PLUS IMPORTANTE !**

```bash
cd backend
notepad .env  # Windows
# OU
nano .env     # Linux/Mac
```

**Copier-coller ce contenu** (voir `CREATE_ENV_FILE.txt` pour le contenu complet) :

```env
ABUSEIPDB_API_KEY=a2e2ed606d95c8882e4c548be391c4418fbf796df2a4c429fab4a25211c06cc976f0db8e024a77be
VIRUSTOTAL_API_KEY=63a8ace54edb588b9781a1f067a27edc014da53f97f56d350bf6eea9a4ebaf8a
AI_DEVICE=cpu
MODEL_LOADING_STRATEGY=startup
```

*(Voir `CREATE_ENV_FILE.txt` pour le contenu complet)*

---

### Étape 2 : Installer les dépendances

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

### Étape 3 : Lancer

**Option A - Script automatique** :
```bash
# À la racine du projet
start.bat  # Windows
```

**Option B - Manuel (2 terminaux)** :

**Terminal 1 - Backend** :
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend** :
```bash
cd frontend
npm run dev
```

---

### Étape 4 : Vérifier

✅ **Backend** : http://localhost:8000/api/docs  
✅ **Frontend** : http://localhost:3000  

**Console backend doit afficher** :
```
✅ Toutes les clés API sont configurées
✅ Modèles IA chargés avec succès
```

---

## 🧪 Premier Test

1. Aller sur http://localhost:3000/network-scan
2. Entrer : `scanme.nmap.org`
3. Cliquer "Démarrer le scan"

**Résultat attendu** :
- 🔍 Toast "Scan en cours..."
- ✅ Ports ouverts détectés (22, 80, 443)
- 📊 Niveau de menace affiché

Si ça marche → **Félicitations, votre plateforme Enterprise est opérationnelle !** 🎉

---

## 📚 Documentation Complète

| Fichier | Description |
|---------|-------------|
| `UPGRADE_SUMMARY.md` | ⭐ Récapitulatif complet des changements |
| `ENTERPRISE_DEPLOYMENT.md` | 🏢 Guide de déploiement production |
| `QUICKSTART.md` | 📖 Guide utilisateur détaillé |
| `TESTS_EXAMPLES.md` | 🧪 50+ exemples de tests |
| `CREATE_ENV_FILE.txt` | 🔑 Instructions pour créer le .env |

---

## ⚠️ Problèmes ?

### "API Key non configurée"
→ Le fichier `.env` n'existe pas dans `backend/`  
→ Créer avec les instructions de `CREATE_ENV_FILE.txt`

### "Modèles IA ne chargent pas"
→ `pip install transformers torch scipy --upgrade`

### "sonner n'est pas défini"
→ `npm install` dans le dossier frontend

---

## ✅ Checklist

- [ ] `.env` créé dans `backend/`
- [ ] `pip install -r requirements.txt`
- [ ] `npm install`
- [ ] Backend démarré sans ⚠️
- [ ] Frontend accessible sur localhost:3000
- [ ] Test Network Scan réussi

---

**🎯 Tout fonctionne ? Consultez `UPGRADE_SUMMARY.md` pour voir toutes les nouveautés !**



