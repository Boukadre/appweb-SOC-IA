# 🧪 Exemples de Tests - Cyber IA Platform

Ce document contient des exemples concrets pour tester chaque module de la plateforme.

---

## 1. 🌐 Network Scan

### Cibles de test

**Domaines légaux à scanner** (pour tests) :
```
scanme.nmap.org
example.com
httpbin.org
```

**Résultats attendus** :
- Ports ouverts : 80, 443, 8080
- Niveau de menace : LOW à MEDIUM
- Vulnérabilités simulées sur services non chiffrés

---

## 2. 🐛 CVE Scanner (NEW)

### URLs de test

**Sites WordPress** (détection CMS + CVE) :
```
https://wordpress.org
https://techcrunch.com
```

**Sites avec technologies variées** :
```
https://httpbin.org  (Python/Flask)
https://github.com     (Ruby/Rails)
https://stackoverflow.com
```

**Résultats attendus** :
- Détection des technologies (serveur, CMS, langages)
- CVE associées si versions vulnérables
- Score de risque global

**Exemple de résultat pour WordPress** :
```json
Technologies:
- WordPress v5.8 (CMS)
- Apache 2.4.41 (Web Server)
- PHP 7.4 (Programming Language)

CVE trouvées:
- CVE-2023-2745 (XSS Vulnerability) - HIGH
- CVE-2022-21661 (SQL Injection) - CRITICAL

Risque global: HIGH
```

---

## 3. 🦠 Malware Analysis

### Noms de fichiers de test

**Fichiers suspects** :
```
suspicious_file.exe
malware.dll
trojan.bat
ransomware.encrypted
```

**Fichiers normaux** :
```
document.pdf
image.jpg
report.docx
```

**Résultats attendus** :
- Analyse basée sur l'extension et le nom
- Score de confiance
- Indicateurs d'analyse

---

## 4. 🎣 Phishing Detection (IA Activée)

### URLs de test

**URLs suspectes** (motifs de phishing) :
```
https://paypa1-secure-login.com
http://g00gle-verify-account.com
https://micros0ft-update.net
http://192.168.1.1/admin?redirect=evil.com
https://bit.ly/suspicious-link
https://app1e-id-verify.com
```

**URLs légitimes** :
```
https://google.com
https://github.com
https://microsoft.com
https://apple.com
```

**Indicateurs détectés** :
- Typosquatting (paypa1 vs paypal)
- IP au lieu de domaine
- URL shorteners
- Mots-clés suspects (login, verify, urgent)

---

### Emails de test

**Email Phishing 1** (Urgence + Demande de credentials) :
```
Subject: URGENT - Account Verification Required

Dear valued customer,

We have detected UNUSUAL ACTIVITY on your account. 
Your account will be SUSPENDED in 24 hours if you 
don't verify your identity immediately.

Click here to verify: http://verify-account-now.com

Please provide your password and credit card information.

If you don't act now, your account will be permanently closed.

Security Team
```

**Résultat attendu** :
- is_phishing: `true`
- confidence: `85-95%`
- threat_level: `HIGH` ou `CRITICAL`
- Indicateurs : Urgency language, Request for sensitive data, Threatening language

---

**Email Phishing 2** (Fausse livraison) :
```
Subject: Your package delivery failed

Dear customer,

We attempted to deliver your package but no one was home.

Click the link below to reschedule:
http://track-delivery-dhl.suspicious.com

Enter your credit card to confirm shipping address.

Package ID: #DHL123456789
```

**Résultat attendu** :
- is_phishing: `true`
- confidence: `75-85%`
- Indicateurs : Request for credit card, Suspicious URL

---

**Email Légitime** :
```
Subject: Your order confirmation

Dear John,

Thank you for your order #12345.

Order Details:
- Product: Laptop
- Amount: $999
- Delivery: 3-5 business days

Track your order at: https://amazon.com/orders/12345

If you have questions, reply to this email.

Best regards,
Customer Service Team
```

**Résultat attendu** :
- is_phishing: `false`
- confidence: `90-95%`
- threat_level: `LOW`

---

## 5. 🔐 Password Analyzer (NEW)

### Mots de passe de test

**Très Faibles (Score: 0)** :
```
password
123456
qwerty
admin
letmein
```

**Résultat attendu** :
- Score: 0/4
- Crack time: "less than a second"
- Warning: ⚠️ Ce mot de passe est très faible

---

**Faibles (Score: 1)** :
```
Password1
Admin123
Welcome!
Summer2024
```

**Résultat attendu** :
- Score: 1/4
- Crack time: "few seconds to minutes"
- Suggestions: Avoid dictionary words, Add more complexity

---

**Moyens (Score: 2)** :
```
MyP@ssw0rd
P@ssw0rd2024
Welcome123!
```

**Résultat attendu** :
- Score: 2/4
- Crack time: "hours to days"
- Suggestions: Use at least 12 characters

---

**Forts (Score: 3)** :
```
Tr0ub4dor&3
MyC0mpl3x!P@ss
G00dP@ssw0rd2024!
```

**Résultat attendu** :
- Score: 3/4
- Crack time: "months to years"

---

**Très Forts (Score: 4)** :
```
correct-horse-battery-staple-2024!
MyS3cur3P@ssw0rdW1thL0ngL3ngth!
Tr0ub4dor&3-WithExtraComplexity!2024
```

**Résultat attendu** :
- Score: 4/4
- Crack time: "centuries"
- Entropy: > 80 bits

---

## 6. 📊 Report Generation

### Test basique

1. Effectuer plusieurs analyses (Network Scan, CVE, Phishing)
2. Noter les IDs des analyses
3. Aller dans Report Generation
4. Sélectionner "Rapport Complet"
5. Format: PDF
6. Générer

**Résultat attendu** :
- report_id généré
- URL de téléchargement
- Taille du fichier

---

## 🎯 Scénarios de Test Complets

### Scénario 1 : Audit de sécurité d'un site

1. **CVE Scanner** : Scanner `https://example.com`
   - Identifier les technologies
   - Lister les CVE

2. **Network Scan** : Scanner `example.com`
   - Vérifier les ports ouverts
   - Détecter les vulnérabilités réseau

3. **Report Generation** : Consolider les résultats

---

### Scénario 2 : Détection de campagne phishing

1. **Phishing Detection (URL)** : Analyser `http://paypa1-verify.com`
   - Score de confiance élevé
   - Typosquatting détecté

2. **Phishing Detection (Email)** : Analyser l'email suspect
   - IA détecte le phishing
   - Recommandations de sécurité

---

### Scénario 3 : Audit de politique de mots de passe

1. **Password Analyzer** : Tester plusieurs mots de passe
   - Tester les mots de passe courants
   - Identifier les faiblesses
   - Appliquer les suggestions

2. Créer un nouveau mot de passe fort
3. Vérifier le score de 4/4

---

## 📈 Métriques de Performance

### Temps de réponse attendus

- **Network Scan** : 2-5 secondes (quick scan)
- **CVE Scanner** : 3-8 secondes
- **Malware Analysis** : < 1 seconde (mock)
- **Phishing Detection** : 1-3 secondes (IA)
- **Password Analyzer** : < 500ms (temps réel)
- **Report Generation** : 1-2 secondes

---

## 🐛 Tests de Gestion d'Erreurs

### Entrées invalides à tester

**Network Scan** :
```
(vide)           → Erreur: Target required
invalid@@@       → Erreur: Invalid format
```

**CVE Scanner** :
```
example.com      → Erreur: URL must start with http:// or https://
not-a-url        → Erreur: Invalid URL
```

**Password Analyzer** :
```
(vide)           → Erreur: Password required
(> 256 chars)    → Erreur: Password too long
```

---

## ✅ Checklist de Tests

- [ ] Backend démarre sans erreur
- [ ] Frontend démarre sans erreur
- [ ] API Health check répond (http://localhost:8000/health)
- [ ] Network Scan fonctionne
- [ ] CVE Scanner détecte les technologies
- [ ] Malware Analysis analyse les fichiers
- [ ] Phishing Detection (URL) fonctionne
- [ ] Phishing Detection (Email) utilise l'IA
- [ ] Password Analyzer calcule en temps réel
- [ ] Report Generation génère des rapports
- [ ] Sidebar affiche tous les modules
- [ ] Gestion d'erreurs fonctionne
- [ ] Loading states s'affichent correctement

---

**Bon testing !** 🧪✅



