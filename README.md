# Orange County Lettings

Application web Django permettant de consulter des locations immobilières (*Holiday Homes*) et des profils d'utilisateurs.

🌐 **Application en production :** [Orange County Lettings](https://python-oc-lettings-fr-omgd.onrender.com)

---

## 🛠️ Développement local

### Prérequis

- Un compte GitHub avec accès au dépôt
- Git
- Python 3.10 ou supérieur
- SQLite3 CLI (facultatif)

Dans la suite de cette documentation, la commande `python` désigne l'interpréteur Python de l'environnement virtuel activé.

### macOS / Linux

#### 1. Cloner le dépôt

```bash
git clone https://github.com/samarkand-fr/Python-OC-Lettings-FR.git
cd oc_lettings
```

> Vérifiez que vous êtes dans le répertoire contenant `manage.py`. Si nécessaire, adaptez la commande `cd` à la structure réelle du dépôt.

#### 2. Créer et activer l'environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

#### 4. Configurer les variables d'environnement

Copiez le fichier d'exemple :

```bash
cp .env.example .env
```

Renseignez les variables nécessaires dans `.env`, notamment `SECRET_KEY` et `SENTRY_DSN`.

Ne partagez jamais vos clés secrètes et ne commitez pas le fichier `.env`.

#### 5. Appliquer les migrations et lancer l'application

```bash
python manage.py migrate
python manage.py runserver
```

L'application est accessible à l'adresse suivante :

[http://localhost:8000](http://localhost:8000)

#### 6. Vérifier la qualité du code

```bash
flake8
```

#### 7. Exécuter les tests et vérifier la couverture

Lancer les tests :

```bash
pytest
```

Mesurer la couverture :

```bash
coverage run -m pytest
```

Générer le rapport et vérifier que la couverture atteint au moins 80 % :

```bash
coverage report --fail-under=80 --omit="*/tests*,*/migrations/*,manage.py,*/wsgi.py,*/asgi.py,conftest.py"
```

#### 8. Accéder au panneau d'administration

Créez un compte administrateur :

```bash
python manage.py createsuperuser
```

Puis accédez au panneau d'administration :

[http://localhost:8000/admin](http://localhost:8000/admin)

---

## 🐳 Exécution locale avec Docker

Docker permet d'exécuter l'application dans un conteneur sans installer directement Python et ses dépendances sur la machine hôte. Docker doit toutefois être installé et démarré.

### Option 1 — Construire l'image localement

```bash
docker build -t oc-lettings:latest .
```

### Option 2 — Lancer le conteneur local

```bash
docker run -d \
  --name oc_lettings_app \
  -p 8000:8000 \
  -e SECRET_KEY="votre_cle_secrete_django" \
  oc-lettings:latest
```

L'application est accessible sur [http://localhost:8000](http://localhost:8000).

### Option 3 — Utiliser l'image publiée sur Docker Hub

```bash
docker run -d --rm \
  --name oc-lettings-container \
  -p 8000:8000 \
  -e SECRET_KEY="votre_cle_secrete" \
  hebanour1998/oc-lettings:latest
```

Cette commande récupère automatiquement l'image si elle n'est pas déjà présente localement, puis lance le conteneur.

**Remarque :** ces commandes supposent que l'image Docker est configurée pour démarrer correctement le serveur Django et que les variables d'environnement nécessaires sont définies.

---

## 🚀 Déploiement et pipeline CI/CD

Le pipeline d'intégration et de déploiement continus (*CI/CD*) est automatisé avec GitHub Actions.

Fichier de configuration :

```text
.github/workflows/ci-cd.yml
```

### Fonctionnement du pipeline

```text
Push / Pull Request
        |
        v
+----------------------------------+
| Job 1 : Tests et linting         |
|                                  |
| - Vérification avec Flake8       |
| - Exécution des tests Pytest     |
| - Vérification de la couverture  |
|   minimale de 80 %               |
+----------------------------------+
        |
        v
Branche master uniquement
        |
        v
+----------------------------------+
| Job 2 : Publication Docker       |
|                                  |
| - Construction de l'image        |
| - Création des tags SHA et latest|
| - Publication sur Docker Hub     |
+----------------------------------+
        |
        v
+----------------------------------+
| Job 3 : Déploiement sur Render   |
|                                  |
| - Appel du Deploy Hook           |
| - Déploiement de la nouvelle     |
|   version de l'application       |
+----------------------------------+
```

### Description des étapes

**Job 1 — Tests et linting**

Exécuté selon les déclencheurs configurés dans le workflow :

- Vérification du style et de la qualité du code avec Flake8.
- Exécution des tests automatisés avec Pytest.
- Vérification du seuil minimal de couverture de 80 %.

**Job 2 — Construction et publication de l'image Docker**

Exécuté uniquement sur la branche `master`, après la réussite du premier job :

- Construction de l'image Docker.
- Attribution de tags basés sur le SHA du commit et sur `latest`.
- Publication de l'image sur Docker Hub.

**Job 3 — Déploiement en production**

Exécuté après la publication réussie de l'image :

- Appel sécurisé du Deploy Hook de Render.
- Déclenchement du déploiement de la nouvelle version.

Sur les branches secondaires et les pull requests, seuls les contrôles prévus par le workflow sont exécutés. La publication et le déploiement sont réservés à la branche `master`, conformément à la configuration décrite ci-dessus.

---

## 🔐 Configuration des secrets GitHub

Pour permettre au pipeline de publier l'image Docker et de déclencher le déploiement, configurez les secrets suivants dans votre dépôt GitHub.

**Chemin :** `Settings → Secrets and variables → Actions → Repository secrets`

| Nom du secret | Description |
|---|---|
| `DOCKER_USERNAME` | Identifiant Docker Hub |
| `DOCKER_PASSWORD` | Jeton d'accès personnel Docker Hub |
| `RENDER_DEPLOY_HOOK_URL` | URL du Deploy Hook du service Render |
| `SECRET_KEY` | Clé secrète Django, si elle est utilisée par le workflow |

Les secrets doivent être configurés dans GitHub avant l'exécution du pipeline. Ne publiez jamais leurs valeurs dans le README ou dans le code source.

---

## ☁️ Configuration du déploiement sur Render

### 1. Créer le service web

1. Connectez-vous à [Render](https://render.com/).
2. Créez un nouveau service web.
3. Sélectionnez le dépôt GitHub ou l'image publiée sur Docker Hub, selon votre méthode de déploiement.
4. Configurez le service conformément au Dockerfile et aux paramètres de démarrage de l'application.

### 2. Désactiver le déploiement automatique

Si le déploiement doit être exclusivement piloté par GitHub Actions, désactivez le déploiement automatique dans les paramètres du service Render.

Cela permet de déclencher le déploiement uniquement après la réussite des vérifications du pipeline.

### 3. Configurer les variables d'environnement

Dans la section **Environment** de Render, ajoutez les variables nécessaires à la production :

| Variable | Description |
|---|---|
| `SECRET_KEY` | Clé secrète Django robuste et confidentielle |
| `DEBUG` | `False` en production |
| `ALLOWED_HOSTS` | Nom d'hôte du service Render, selon le format attendu par Django |
| `SENTRY_DSN` | DSN du projet Sentry, si la surveillance des erreurs est activée |

Les secrets configurés dans GitHub ne sont pas automatiquement transmis à Render. Les variables nécessaires à l'application doivent donc également être configurées dans l'environnement Render.

### 4. Configurer le Deploy Hook

1. Ouvrez les paramètres du service Render.
2. Récupérez l'URL du Deploy Hook.
3. Ajoutez cette URL dans les secrets GitHub sous le nom `RENDER_DEPLOY_HOOK_URL`.

Cette URL doit rester confidentielle.

### 5. Déclencher un déploiement

Après avoir configuré le pipeline :

1. Effectuez vos modifications dans le code.
2. Créez un commit et poussez-le sur la branche `master`.
3. Vérifiez que les tests et le linting réussissent.
4. Vérifiez que l'image Docker est publiée sur Docker Hub.
5. Confirmez que le déploiement est déclenché sur Render.
6. Accédez à l'application en production :

[Orange County Lettings](https://python-oc-lettings-fr-omgd.onrender.com)

---

## 📚 Documentation technique (Sphinx)

La documentation complète du projet est générée à l'aide de **Sphinx** et utilise le thème officiel **Read the Docs**.

### 1. Consulter la documentation en local

Pour générer la documentation HTML en local :

```bash
sphinx-build -b html docs docs/_build/html
```

Ou en utilisant le Makefile dans le dossier `docs/` :

```bash
cd docs
make html
```

Ouvrez ensuite le fichier `docs/_build/html/index.html` dans votre navigateur web :

```bash
# macOS
open docs/_build/html/index.html

# Linux
xdg-open docs/_build/html/index.html

# Windows
start docs/_build/html/index.html
```

### 2. Contenu de la documentation

La documentation est structurée en plusieurs guides détaillés :

- **Description du projet** : Contexte, objectifs et présentation fonctionnelle.
- **Guide d'installation** : Prérequis, environnement virtuel, configuration `.env` et dépendances.
- **Démarrage rapide** : Lancement du serveur local, navigation et points de contrôle.
- **Base de données et modèles** : Schéma relationnel, diagramme ORM, détails des modèles et migrations.
- **Architecture et technologies** : Architecture modulaire, intergiciels WhiteNoise, surveillance Sentry et journalisation.
- **Déploiement et CI/CD** : Conteneurisation Docker, jobs GitHub Actions et hébergement Render.

---

## 📋 Bonnes pratiques

- Ne stockez jamais les clés secrètes dans le dépôt Git.
- Utilisez des variables d'environnement pour les paramètres sensibles.
- Exécutez les tests avant chaque déploiement.
- Bloquez le déploiement si les tests échouent ou si la couverture est inférieure au seuil défini.
- Utilisez Sentry pour faciliter le suivi et le diagnostic des erreurs.
- Vérifiez la persistance de la base SQLite en environnement Docker et en production.
- Séparez les configurations de développement et de production.
