Guide d'installation et prérequis
==================================

Prérequis système
-----------------

Pour installer et exécuter l'application en environnement local, les outils suivants sont requis :

* **Python** : version 3.10 ou supérieure.
* **Git** : pour le clonage et la gestion des versions.
* **SQLite 3** : moteur de base de données inclus par défaut avec Python.
* **Docker** *(optionnel mais recommandé)* : pour tester l'application dans son conteneur de production.

Clonage du dépôt
----------------

Clonez le projet depuis GitHub et placez-vous dans le répertoire de travail :

.. code-block:: bash

   git clone https://github.com/samarkand-fr/Python-OC-Lettings-FR.git
   cd Python-OC-Lettings-FR

Création et activation de l'environnement virtuel
-------------------------------------------------

Il est fortement recommandé d'isoler les dépendances du projet dans un environnement virtuel dédié :

* **Sous macOS et Linux** :

  .. code-block:: bash

     python3 -m venv venv
     source venv/bin/activate

* **Sous Windows (PowerShell)** :

  .. code-block:: powershell

     python -m venv venv
     .\venv\Scripts\Activate.ps1

* **Sous Windows (Invite de commandes cmd)** :

  .. code-block:: bat

     python -m venv venv
     .\venv\Scripts\activate.bat

Installation des dépendances
----------------------------

Mettez à niveau le gestionnaire de paquets ``pip`` et installez l'ensemble des bibliothèques requises :

.. code-block:: bash

   python -m pip install --upgrade pip
   pip install -r requirements.txt

Configuration des variables d'environnement
-------------------------------------------

L'application utilise la bibliothèque ``python-dotenv`` pour charger ses paramètres depuis un fichier ``.env`` situé à la racine du projet.

1. Créez votre fichier ``.env`` à partir du modèle fourni :

   .. code-block:: bash

      cp .env.example .env

2. Éditez le fichier ``.env`` et renseignez les variables nécessaires :

   .. code-block:: ini

      SECRET_KEY=votre_cle_secrete_django_securisee
      DEBUG=True
      ALLOWED_HOSTS=localhost,127.0.0.1,testserver
      SENTRY_DSN=https://votre_cle@sentry.io/votre_projet
      SENTRY_TRACES_SAMPLE_RATE=1.0

.. note::
   La variable ``SECRET_KEY`` est strictement obligatoire. Si elle n'est pas définie, Django lèvera une exception explicite au démarrage afin d'empêcher toute exécution non sécurisée.

Application des migrations de base de données
---------------------------------------------

La base de données SQLite préremplie avec le jeu de données d'exemple est fournie avec le projet (``oc-lettings-site.sqlite3``). Pour vous assurer que le schéma est à jour :

.. code-block:: bash

   python manage.py migrate

Exécution des vérifications et des tests
----------------------------------------

Avant de lancer le serveur, vous pouvez vérifier la conformité du code et la validité des tests :

* **Vérification du style PEP 8 avec Flake8** :

  .. code-block:: bash

     flake8

* **Exécution de la suite de tests avec Pytest** :

  .. code-block:: bash

     pytest

* **Vérification de la couverture de code** :

  .. code-block:: bash

     coverage run -m pytest
     coverage report --fail-under=80 --omit="*/tests*,*/migrations/*,manage.py,*/wsgi.py,*/asgi.py,conftest.py"
