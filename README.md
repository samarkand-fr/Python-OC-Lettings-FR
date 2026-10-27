# Orange County Lettings

Application web de réservation et de consultation de locations immobilières (Holiday Homes) et de profils d'utilisateurs.

---

## 🛠️ Développement local

### Prérequis

- Compte GitHub avec accès au repository
- Git CLI
- SQLite3 CLI
- Python version 3.10 ou supérieure

Dans la suite de la documentation, la commande `python` fait référence à l'interpréteur de votre environnement virtuel.

### macOS / Linux

#### 1. Cloner le repository

```bash
git clone https://github.com/samarkand-fr/Python-OC-Lettings-FR.git
cd oc_lettings
```

#### 2. Créer et activer l'environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

#### 4. Variables d'environnement

Copiez le modèle `.env.example` en `.env` :

```bash
cp .env.example .env
```

Renseignez vos valeurs dans `.env` (notamment `SECRET_KEY` et `SENTRY_DSN`).

#### 5. Lancer l'application

```bash
python manage.py migrate
python manage.py runserver
```

Accédez au site sur `http://localhost:8000`.

#### 6. Linting (Flake8)

```bash
flake8
```

#### 7. Tests & Couverture (Coverage)

```bash
# Lancer les tests unitaires et d'intégration
pytest

# Calculer et vérifier le taux de couverture (> 80%)
coverage run -m pytest
coverage report --omit="*/tests*,*/migrations/*,manage.py,*/wsgi.py,*/asgi.py,conftest.py"
```

#### 8. Panel d'administration

- Rendez-vous sur `http://localhost:8000/admin`.
- Vous pouvez créer un administrateur avec `python manage.py createsuperuser`.

---

## 🐳 Exécution locale avec Docker (Commande unique)

Vous pouvez lancer l'application localement via Docker sans avoir besoin d'installer Python :

### 1. Construire l'image localement

```bash
docker build -t oc-lettings:latest .
```

### 2. Lancer le conteneur (Commande unique)

```bash
docker run -d --name oc_lettings_app -p 8000:8000 -e SECRET_KEY="votre_cle_secrete_django" oc-lettings:latest
```

Accédez à l'application sur `http://localhost:8000`.

### 3. Exécuter l'image depuis Docker Hub en une seule commande

Pour récupérer directement l'image publiée sur Docker Hub et la lancer :

```bash
docker run -d --rm --name oc-lettings-container -p 8000:8000 -e SECRET_KEY="votre_cle_secrete" <VOTRE_DOCKER_USERNAME>/oc-lettings:latest
```

---

## 🚀 Déploiement et Pipeline CI/CD

### Récapitulatif haut niveau

Le pipeline d'intégration et de déploiement continus (CI/CD) est géré automatiquement par **GitHub Actions** (`.github/workflows/ci-cd.yml`) :

[ Push / Pull Request ]
          │
          ▼
┌────────────────────────────────────────────────────────┐
│ Job 1 : Test & Lint (Toutes les branches)             │
│  - Contrôle PEP8 avec Flake8                           │
│  - Exécution des tests avec Pytest                     │
│  - Vérification stricte du taux de couverture (> 80%)  │
└────────────────────────────────────────────────────────┘
          │
          ▼ (Uniquement sur la branche 'master' et si Job 1 réussit)
┌────────────────────────────────────────────────────────┐
│ Job 2 : Conteneurisation Docker Hub                    │
│  - Construction de l'image Docker multi-plateforme     │
│  - Tag de l'image avec le SHA du commit et 'latest'    │
│  - Push automatique sur le registre Docker Hub         │
└────────────────────────────────────────────────────────┘
          │
          ▼ (Uniquement sur la branche 'master' et si Job 2 réussit)
┌────────────────────────────────────────────────────────┐
│ Job 3 : Déploiement en Production (Render)             │
│  - Appel sécurisé du Webhook Deploy Hook de Render     │
│  - Déploiement de la nouvelle image Docker en direct   │
└────────────────────────────────────────────────────────┘

- **Sur les branches secondaires / Pull Requests** : seuls les tests et le linting s'exécutent. Aucun conteneur n'est construit et aucun déploiement n'a lieu.
- **Sur la branche `master`** : si et seulement si les tests réussissent, l'image Docker est poussée sur Docker Hub, puis le déploiement sur Render est déclenché.

### Configuration requise (GitHub Secrets)

Pour que le pipeline fonctionne correctement sur votre repository GitHub, ajoutez les secrets suivants dans **Settings > Secrets and variables > Actions > Repository secrets** :

| Nom du Secret | Description | Exemple |
| :--- | :--- | :--- |
| `DOCKER_USERNAME` | Votre identifiant Docker Hub | `monlogin` |
| `DOCKER_PASSWORD` | Votre Personal Access Token Docker Hub (recommandé) ou mot de passe | `dckr_pat_...` |
| `RENDER_DEPLOY_HOOK_URL` | L'URL du Deploy Hook de votre service Web Render | `https://api.render.com/deploy/srv-xxxx?key=yyyy` |
| `SECRET_KEY` | Clé secrète Django pour la production | *(chaîne aléatoire complexe)* |

### Étapes nécessaires pour configurer le déploiement sur Render

1. **Créer un service Web sur Render** :
   - Rendez-vous sur [Render.com](https://render.com/) et connectez votre compte GitHub.
   - Cliquez sur **New + > Web Service**.
   - Choisissez l'option **"Deploy an existing image from a registry"** ou connectez votre repository GitHub en sélectionnant l'environnement **Docker**.
2. **Désactiver le déploiement automatique sur Render** :
   - Dans les paramètres du service sur Render (**Settings**), réglez **Auto-Deploy** sur **"No"**.
   - *Raison :* Le déploiement ne doit être déclenché **que par GitHub Actions** une fois tous les tests validés avec succès.
3. **Récupérer le Deploy Hook** :
   - Dans **Settings > Deploy Hook**, copiez l'URL fournie (ex: `https://api.render.com/deploy/srv-...`).
   - Ajoutez cette URL dans les secrets de votre repository GitHub sous le nom `RENDER_DEPLOY_HOOK_URL`.
4. **Définir les variables d'environnement sur Render** :
   - Dans l'onglet **Environment** de votre service Render, ajoutez :
     - `SECRET_KEY` : une clé secrète Django forte.
     - `DEBUG` : `False`
     - `ALLOWED_HOSTS` : votre URL Render (ex: `mon-projet.onrender.com,localhost`)
     - `SENTRY_DSN` : votre clé DSN Sentry
5. **Déclencher le déploiement** :
   - Effectuez un commit et poussez sur la branche `master`.
   - Observez le pipeline GitHub Actions s'exécuter avec succès, puis accédez à votre application en direct sur votre URL publique Render.
