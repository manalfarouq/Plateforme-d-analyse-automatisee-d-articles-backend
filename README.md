# Hybrid-Analyzer Platform - Backend

[![Tests](https://github.com/manalfarouq/Plateforme-d-analyse-automatisee-d-articles-backend/workflows/Tests/badge.svg)](https://github.com/manalfarouq/Plateforme-d-analyse-automatisee-d-articles-backend/actions)
[![Docker](https://github.com/manalfarouq/Plateforme-d-analyse-automatisee-d-articles-backend/workflows/Docker%20Build/badge.svg)](https://github.com/manalfarouq/Plateforme-d-analyse-automatisee-d-articles-backend/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## Table des Matières

- [Contexte du Projet](#-contexte-du-projet)
- [Architecture](#-architecture)
- [Technologies Utilisées](#-technologies-utilisées)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [API Documentation](#-api-documentation)
- [Tests](#-tests)
- [CI/CD](#-cicd)
- [Gestion des Erreurs](#-gestion-des-erreurs)
- [Limites Techniques](#-limites-techniques)
- [Contribution](#-contribution)

---

## Contexte du Projet

### Problématique
L'agence spécialisée en media monitoring traite manuellement des centaines d'articles quotidiennement, ce qui est :
-  **Lent** - Traitement manuel chronophage
-  **Coûteux** - Mobilisation importante de ressources humaines
-  **Peu fiable** - Difficile à standardiser à grande échelle
-  **Dépendant** - Expertise humaine nécessaire pour chaque analyse

### Solution
**Hybrid-Analyzer** automatise l'analyse en orchestrant deux services IA :

1. **Classification Zero-Shot** (Hugging Face)

2. **Analyse Contextuelle** (API Gemini)
   - Génération de résumés ciblés
   - Évaluation du ton (positif, négatif, neutre)
   - Contexte enrichi par la classification HF

---

## Architecture

### Architecture Microservices
```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Client)                     │
│                    (Next.js / React / HTML)                  │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP/REST + JWT
                 │
┌────────────────▼────────────────────────────────────────────┐
│                     API Gateway / Load Balancer              │
└────────┬────────────────────┬─────────────────┬─────────────┘
         │                    │                 │
         │                    │                 │
┌────────▼──────────┐ ┌──────▼──────────┐ ┌───▼──────────────┐
│  Service Auth     │ │ Service Analyse │ │ Service Gemini   │
│  (Port 8001)      │ │  (Port 8002)    │ │  (Port 8003)     │
│                   │ │                 │ │                  │
│ • JWT Auth        │ │ • HF API        │ │ • Gemini API     │
│ • User Management │ │ • Orchestration │ │ • Summarization  │
│ • PostgreSQL      │ │ • Pipeline      │ │ • Tone Analysis  │
└───────────────────┘ └─────────────────┘ └──────────────────┘
         │
         │
┌────────▼──────────────────────────────────────────────────┐
│                    PostgreSQL Database                     │
│                                                            │
│  • users (auth, profiles)                                 │
│  • analyse_logs (history, results)                        │
└───────────────────────────────────────────────────────────┘
```

### Workflow d'Analyse
```
┌──────────┐
│  Client  │
└────┬─────┘
     │ 1. POST /analyze (+ JWT token)
     │
┌────▼────────────┐
│ Service Analyse │
└────┬────────────┘
     │
     │ 2. Classification Zero-Shot
     ├──────────────────────────────┐
     │                              │
┌────▼────────────┐         ┌──────▼──────────┐
│ Hugging Face    │         │ Service Gemini  │
│ API             │         │                 │
│ (bart-mnli)     │         │ 4. Synthèse +   │
└────┬────────────┘         │    Ton Analysis │
     │                      └──────┬──────────┘
     │ 3. Catégorie + Score        │
     └──────────────┬───────────────┘
                    │
              ┌─────▼──────┐
              │  Agrégation│
              │  Résultats │
              └─────┬──────┘
                    │
              ┌─────▼──────────────────┐
              │ 5. JSON Structuré :    │
              │  • Catégorie           │
              │  • Score               │
              │  • Résumé              │
              │  • Ton                 │
              └────────────────────────┘
```

---

## Technologies Utilisées

### Backend
| Technologie | Version | Usage |
|-------------|---------|-------|
| **Python** | 3.10+ | Langage principal |
| **FastAPI** | 0.104+ | Framework web asynchrone |
| **SQLAlchemy** | 2.0+ | ORM pour PostgreSQL |
| **Pydantic** | 2.0+ | Validation de données |
| **PyJWT** | 2.8+ | Authentification JWT |
| **bcrypt** | 4.0+ | Hachage des mots de passe |
| **httpx** | 0.25+ | Client HTTP asynchrone |

### Base de Données
| Technologie | Version | Usage |
|-------------|---------|-------|
| **PostgreSQL** | 15+ | Base de données relationnelle |
| **psycopg2** | 2.9+ | Driver PostgreSQL |

### APIs Externes
| Service | Modèle/Version | Usage |
|---------|----------------|-------|
| **Hugging Face Inference API** | `facebook/bart-large-mnli` | Classification Zero-Shot |
| **Google Gemini API** | `gemini-pro` | Analyse contextuelle et synthèse |

### DevOps CI/CD
| Outil | Usage |
|-------|-------|
| **Docker** | Containerisation |
| **Docker Compose** | Orchestration multi-conteneurs |
| **GitHub Actions** | CI/CD (tests, builds) |
| **pytest** | Tests unitaires |


---

## Fonctionnalités

### Authentification (Service Auth)
- ✅ Inscription utilisateur (`POST /Signup`)
- ✅ Connexion avec JWT (`POST /Login`)
- ✅ Hachage sécurisé des mots de passe (bcrypt)
- ✅ Validation des tokens JWT
- ✅ Gestion des utilisateurs

### Analyse Intelligente (Service Analyse)
- ✅ Classification Zero-Shot via Hugging Face
  - Catégorisation automatique (Finance, RH, IT, Opérations, Marketing, etc.)
  - Scores de confiance
- ✅ Analyse contextuelle via Gemini
  - Résumés ciblés selon la catégorie
  - Détection du ton (positif, neutre, négatif)
- ✅ Pipeline d'analyse complet (`POST /analyse-complet`)
- ✅ Historique des analyses (`GET /history`)
- ✅ Filtrage par catégorie (`GET /filtrer`)

### Gestion des Données
- ✅ Stockage PostgreSQL
- ✅ Logs d'analyse persistants
- ✅ Relations utilisateur-analyses

### Qualité & Fiabilité
- ✅ Tests unitaires automatisés
- ✅ Gestion complète des erreurs
- ✅ Logging structuré
- ✅ Validation des données (Pydantic)
- ✅ CI/CD avec GitHub Actions

---

## Installation

### Prérequis
- **Python 3.10+**
- **PostgreSQL 15+**
- **Docker & Docker Compose** (optionnel)
- **Git**

### 1. Cloner le Repository
```bash
git clone https://github.com/manalfarouq/Plateforme-d-analyse-automatisee-d-articles-backend.git
cd Plateforme-d-analyse-automatisee-d-articles-backend
```

### 2. Installation avec Docker (Recommandé)
```bash
# Créer les fichiers .env pour chaque service
cp service-auth/.env.example service-auth/.env
cp service-gemini/.env.example service-gemini/.env
cp service-analyse/.env.example service-analyse/.env

# Modifier les .env avec vos clés API

# Lancer tous les services
docker-compose up -d
```

### 3. Installation Manuelle

#### Service Auth
```bash
cd service-auth
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Service Gemini
```bash
cd service-gemini
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Service Analyse
```bash
cd service-analyse
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Configuration

### Variables d'Environnement

#### Service Auth (`.env`)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/hybrid_analyzer

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database Components
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hybrid_analyzer
DB_USER=your_user
DB_PASSWORD=your_password
```

#### Service Gemini (`.env`)
```env
GEMINI_API_KEY=your-gemini-api-key-here
```

#### Service Analyse (`.env`)
```env
# Hugging Face
HF_TOKEN=your-huggingface-token-here

# Gemini (si appel direct)
GEMINI_API_KEY=your-gemini-api-key-here

# Service URLs (si microservices séparés)
GEMINI_SERVICE_URL=http://localhost:8003
AUTH_SERVICE_URL=http://localhost:8001
```

### Obtenir les Clés API

#### Hugging Face Token
1. Créer un compte sur [huggingface.co](https://huggingface.co)
2. Aller dans **Settings → Access Tokens**
3. Créer un nouveau token avec permissions `read`

#### Gemini API Key
1. Créer un projet sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Générer une clé API
3. Copier la clé dans votre `.env`

---

## Utilisation

### Lancer les Services

#### Avec Docker Compose
```bash
docker-compose up -d
```

Services disponibles :
- **Service Auth**: `http://localhost:8001`
- **Service Analyse**: `http://localhost:8002`
- **Service Gemini**: `http://localhost:8003`
- **PostgreSQL**: `localhost:5432`

#### Manuellement
```bash
# Terminal 1 - Service Auth
cd service-auth
uvicorn app.main:app --reload --port 8001

# Terminal 2 - Service Gemini
cd service-gemini
uvicorn app.main:app --reload --port 8003

# Terminal 3 - Service Analyse
cd service-analyse
uvicorn app.main:app --reload --port 8002
```

### Initialiser la Base de Données
```bash
cd service-auth
python create_tables.py
```

---

## API Documentation

### Service Auth (`http://localhost:8001`)

#### 1. Inscription
```http
POST /Signup
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Réponse** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### 2. Connexion
```http
POST /Login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securePassword123"
}
```

**Réponse** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe"
  }
}
```

#### 3. Liste des Utilisateurs
```http
GET /users
Authorization: Bearer <token>
```

---

### Service Analyse (`http://localhost:8002`)

#### 1. Classification Simple (Hugging Face)
```http
POST /analyze
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "Apple annonce une augmentation de 15% de son chiffre d'affaires trimestriel."
}
```

**Réponse** (200 OK):
```json
{
  "categorie": "Finance",
  "score": 0.92,
  "labels_scores": {
    "Finance": 0.92,
    "IT": 0.05,
    "Operations": 0.03
  }
}
```

#### 2. Analyse Complète (HF + Gemini)
```http
POST /analyse-complet
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "Apple annonce une augmentation de 15% de son chiffre d'affaires trimestriel grâce aux ventes d'iPhone."
}
```

**Réponse** (200 OK):
```json
{
  "classification": {
    "categorie": "Finance",
    "score": 0.92
  },
  "analyse_gemini": {
    "resume": "Apple enregistre une croissance financière significative de 15% sur le trimestre, principalement portée par les ventes d'iPhone.",
    "ton": "positif",
    "details": "Performance financière exceptionnelle avec une forte demande pour les produits phares."
  }
}
```

#### 3. Historique des Analyses
```http
GET /history
Authorization: Bearer <token>
```

**Réponse** (200 OK):
```json
{
  "analyses": [
    {
      "id": 1,
      "texte_original": "Apple annonce...",
      "categorie": "Finance",
      "resume": "Apple enregistre...",
      "ton": "positif",
      "created_at": "2024-12-10T14:30:00Z"
    }
  ]
}
```

#### 4. Filtrer par Catégorie
```http
GET /filtrer?categorie=Finance
Authorization: Bearer <token>
```

---

### Service Gemini (`http://localhost:8003`)

#### Analyse Contextuelle
```http
POST /analyze
Content-Type: application/json

{
  "text": "Apple annonce une augmentation de 15%...",
  "categorie": "Finance"
}
```

**Réponse** (200 OK):
```json
{
  "resume": "Apple enregistre une croissance financière...",
  "ton": "positif",
  "details": "Performance exceptionnelle..."
}
```

---

## Tests

### Structure des Tests
```
tests/
├── service-auth/
│   └── test_auth.py          # Tests auth (register, login)
├── service-gemini/
│   └── test_gemini.py        # Tests Gemini avec mocks
└── service-analyse/
    ├── test_analyse.py       # Tests HF classification
    └── test_pipeline.py      # Tests pipeline complet
```

### Lancer les Tests

#### Tous les Tests
```bash
# Avec Docker
docker-compose run service-auth pytest
docker-compose run service-gemini pytest
docker-compose run service-analyse pytest

# Manuellement
cd service-auth && pytest -v
cd service-gemini && pytest -v
cd service-analyse && pytest -v
```

#### Tests Spécifiques
```bash
# Test Auth uniquement
cd service-auth
pytest tests/test_auth.py -v

# Test avec coverage
pytest --cov=app tests/ --cov-report=html
```

### Mocks Utilisés

Les tests utilisent des **mocks complets** pour éviter les appels API réels :

- ✅ **Mock Hugging Face**: Réponses de classification simulées
- ✅ **Mock Gemini**: Analyses générées localement
- ✅ **Mock PostgreSQL**: Base de données de test isolée

---

## CI/CD

### GitHub Actions Workflows

#### 1. Tests Automatisés (`.github/workflows/tests.yml`)
```yaml
# Déclenché sur push et pull_request
# Teste les 3 services en parallèle
# PostgreSQL en service container pour service-auth
```

**Jobs**:
- ✅ `test-auth` - Tests avec PostgreSQL 15
- ✅ `test-gemini` - Tests avec mock Gemini
- ✅ `test-analyse` - Tests avec mock HF

#### 2. Docker Build (`.github/workflows/docker.yml`)
```yaml
# Déclenché sur push et pull_request
# Build des 3 images Docker
```

**Jobs**:
- ✅ Build `service-auth:latest`
- ✅ Build `service-gemini:latest`
- ✅ Build `service-analyse:latest`

### Badges de Status

[![Tests](https://github.com/manalfarouq/Plateforme-d-analyse-automatisee-d-articles-backend/workflows/Tests/badge.svg)](https://github.com/manalfarouq/Plateforme-d-analyse-automatisee-d-articles-backend/actions)
[![Docker](https://github.com/manalfarouq/Plateforme-d-analyse-automatisee-d-articles-backend/workflows/Docker%20Build/badge.svg)](https://github.com/manalfarouq/Plateforme-d-analyse-automatisee-d-articles-backend/actions)

---

### Codes HTTP Utilisés

| Code | Signification | Usage |
|------|---------------|-------|
| 200 | OK | Succès |
| 201 | Created | Ressource créée |
| 400 | Bad Request | Données invalides |
| 401 | Unauthorized | Token manquant/invalide |
| 404 | Not Found | Ressource introuvable |
| 500 | Internal Error | Erreur serveur |
| 502 | Bad Gateway | Erreur API externe |
| 504 | Gateway Timeout | Timeout API externe |

---

## Limites Techniques

### 1. Dépendance aux APIs Externes

**Hugging Face**:
- ⚠️ Rate limits (appels/heure)
- ⚠️ Latence variable (modèle on-demand)
- ⚠️ Indisponibilité ponctuelle

**Solution**: Retry logic, cache, fallback local

**Gemini**:
- ⚠️ Quotas quotidiens
- ⚠️ Coût par requête
- ⚠️ Réponses parfois incohérentes

**Solution**: Validation des réponses, retry, logging

### 2. Performance

- ⏱**Latence totale**: 3-10 secondes (HF + Gemini séquentiels)
- **Throughput**: ~10-20 requêtes/minute (rate limits)
