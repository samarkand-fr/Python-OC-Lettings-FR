Déploiement et pipeline CI/CD
==============================

Conteneurisation avec Docker
----------------------------

L'application est entièrement conteneurisée afin d'assurer une parfaite parité entre l'environnement de développement et l'environnement de production.

Structure du ``Dockerfile``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le fichier ``Dockerfile`` à la racine utilise une image officielle Python 3.10 légère (``python:3.10-slim``) :

.. code-block:: dockerfile

   # Image de base
   FROM python:3.10-slim

   # Variables d'environnement Python
   ENV PYTHONDONTWRITEBYTECODE=1 \
       PYTHONUNBUFFERED=1 \
       PORT=8000

   WORKDIR /app

   # Installation des dépendances
   COPY requirements.txt /app/
   RUN pip install --no-cache-dir --upgrade pip && \
       pip install --no-cache-dir -r requirements.txt

   # Copie du code applicatif
   COPY . /app/

   # Rassemblement des fichiers statiques (WhiteNoise)
   RUN SECRET_KEY="temporary-build-key-for-collectstatic" python manage.py collectstatic --noinput

   EXPOSE 8000

   # Démarrage : exécution des migrations puis lancement du serveur Gunicorn
   CMD ["sh", "-c", "python manage.py migrate && gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]

Commandes utiles Docker
~~~~~~~~~~~~~~~~~~~~~~~

* **Construction locale de l'image** :

  .. code-block:: bash

     docker build -t oc-lettings:latest .

* **Exécution locale du conteneur** :

  .. code-block:: bash

     docker run -d -p 8000:8000 \
       -e SECRET_KEY="cle-locale-de-test-tres-longue-et-securisee" \
       -e DEBUG=False \
       -e ALLOWED_HOSTS="localhost,127.0.0.1" \
       --name oc_lettings_container \
       oc-lettings:latest

* **Arrêt et suppression du conteneur** :

  .. code-block:: bash

     docker stop oc_lettings_container
     docker rm oc_lettings_container

Pipeline d'intégration et déploiement continu (CI/CD)
-----------------------------------------------------

Le pipeline est piloté de façon entièrement automatisée par **GitHub Actions** via le fichier de workflow ``.github/workflows/ci-cd.yml``.

Schéma du cycle de vie
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Déclencheur : Push ou Pull Request
                 |
                 v
   +-----------------------------------------------+
   | Job 1 : Lint & Test Suite (ubuntu-22.04)      |
   | - Installation Python 3.10                    |
   | - Vérification Flake8 (PEP 8)                 |
   | - Exécution de la suite Pytest                |
   | - Contrôle de la couverture (> 80 %)          |
   +-----------------------+-----------------------+
                           |
            Succès du Job 1 ET Branche 'master'
                           |
                           v
   +-----------------------------------------------+
   | Job 2 : Build & Push Docker Image             |
   | - Authentification sur Docker Hub             |
   | - Construction de l'image                     |
   | - Publication sous les tags <commit_sha>      |
   |   et 'latest'                                 |
   +-----------------------+-----------------------+
                           |
                    Succès du Job 2
                           |
                           v
   +-----------------------------------------------+
   | Job 3 : Deploy to Production (Render)         |
   | - Appel sécurisé du Webhook Deploy Hook       |
   | - Re-déploiement automatisé du conteneur      |
   +-----------------------------------------------+

Détail des 3 Jobs
~~~~~~~~~~~~~~~~~

1. **Job 1 : Lint & Test Suite**
   - S'exécute sur **toutes les branches** à chaque ``push`` ou ``pull_request``.
   - Installe l'environnement Python 3.10 et les dépendances du projet.
   - Lance le linter Flake8 : bloque le pipeline en cas de non-respect de PEP 8.
   - Exécute les 25 tests unitaires et d'intégration avec Pytest.
   - Vérifie que la couverture de code globale dépasse le seuil strict de 80 %.

2. **Job 2 : Build & Push Docker Image**
   - Ne s'exécute que sur la branche ``master``, après validation complète du Job 1.
   - Se connecte de manière sécurisée au registre Docker Hub.
   - Construit l'image de production et la publie sous deux étiquettes : le SHA unique du commit Git et le tag flottant ``latest``.

3. **Job 3 : Deploy to Production**
   - Ne s'exécute que sur la branche ``master``, après publication réussie de l'image Docker.
   - Déclenche le Webhook de déploiement (Deploy Hook) du service cloud Render.
   - Render télécharge la nouvelle image conteneur et redémarre le service avec un temps d'indisponibilité nul (*zero-downtime deployment*).

Secrets GitHub nécessaires
--------------------------

Pour que le pipeline fonctionne en autonomie, les variables secrètes suivantes doivent être configurées dans l'interface de GitHub (``Settings > Secrets and variables > Actions > Repository secrets``) :

* ``DOCKER_USERNAME`` : Nom d'utilisateur du compte Docker Hub.
* ``DOCKER_PASSWORD`` : Jeton d'accès personnel (Personal Access Token) généré sur Docker Hub.
* ``RENDER_DEPLOY_HOOK_URL`` : URL secrète du Deploy Hook fournie par les paramètres du service Web sur Render.
* ``SECRET_KEY`` : Clé secrète Django robuste utilisée par l'application.

Hébergement en production sur Render
------------------------------------

L'application est déployée en continu et accessible publiquement à l'adresse suivante :

`https://python-oc-lettings-fr-omgd.onrender.com <https://python-oc-lettings-fr-omgd.onrender.com>`_

Sur la plateforme Render, les variables d'environnement suivantes sont configurées dans l'onglet **Environment** :

* ``SECRET_KEY`` : Clé secrète de production.
* ``DEBUG`` : ``False``
* ``ALLOWED_HOSTS`` : ``python-oc-lettings-fr-omgd.onrender.com,.onrender.com,localhost``
* ``SENTRY_DSN`` : DSN du projet Sentry pour la surveillance continue.
