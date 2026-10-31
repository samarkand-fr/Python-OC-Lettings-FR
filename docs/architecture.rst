Architecture modulaire et technologies
=========================================

Principes directeurs de conception
----------------------------------

Le projet Orange County Lettings est structuré selon les principes fondamentaux du génie logiciel :

* **Séparation des responsabilités (SoC - Separation of Concerns)** : Chaque module logiciel se concentre sur une thématique fonctionnelle précise.
* **Forte cohésion** : Tout le code lié à un domaine (modèles, vues, gabarits, routes, tests, configuration d'administration) réside à l'intérieur de la même application.
* **Faible couplage** : L'application ``lettings`` ne dépend pas de l'application ``profiles``, et vice-versa. Chacune peut être développée, testée, déployée ou refondue de façon autonome.

Organisation des modules applicatifs
------------------------------------

L'arborescence du projet s'articule autour de trois applications Django distinctes :

1. ``oc_lettings_site`` (Application racine / Orchestration)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* **Rôle** : Point d'entrée principal du projet Django.
* **Fichiers clés** :
  - ``settings.py`` : Configuration globale (applications installées, intergiciels, base de données, logging, Sentry, WhiteNoise, gestion des environnements).
  - ``urls.py`` : Routage de premier niveau avec espaces de noms (``namespace='lettings'`` et ``namespace='profiles'``), déclaration des gestionnaires d'erreur personnalisés (``handler404``, ``handler500``) et de la route de test Sentry.
  - ``views.py`` : Vue de la page d'accueil (``index``) et gestionnaires d'erreurs HTTP 404 et 500.
  - ``wsgi.py`` et ``asgi.py`` : Interfaces avec les serveurs d'application WSGI (Gunicorn en production) et ASGI.

2. ``lettings`` (Gestion des hébergements de vacances)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* **Rôle** : Encapsule l'ensemble du cycle de vie des biens locatifs et de leurs adresses.
* **Fichiers clés** :
  - ``models.py`` : Définition des entités ``Address`` et ``Letting``.
  - ``views.py`` : Vues ``index`` (catalogue) et ``letting`` (fiche détaillée) intégrant des blocs ``try/except`` et des journaux d'événements.
  - ``urls.py`` : Déclaration des routes avec l'espace de noms ``app_name = 'lettings'``.
  - ``templates/lettings/`` : Gabarits HTML spécifiques aux locations.
  - ``tests.py`` : Tests unitaires et d'intégration validant les modèles et les vues.
  - ``admin.py`` : Configuration de l'interface d'administration Django.

3. ``profiles`` (Gestion des profils utilisateurs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* **Rôle** : Encapsule les informations associées aux utilisateurs du service.
* **Fichiers clés** :
  - ``models.py`` : Définition de l'entité ``Profile`` en liaison univoque avec ``User``.
  - ``views.py`` : Vues ``index`` (annuaire) et ``profile`` (profil individuel).
  - ``urls.py`` : Déclaration des routes avec l'espace de noms ``app_name = 'profiles'``.
  - ``templates/profiles/`` : Gabarits HTML spécifiques aux profils.
  - ``tests.py`` : Tests unitaires et d'intégration dédiés.
  - ``admin.py`` : Configuration d'administration.

Gestion des fichiers statiques avec WhiteNoise
----------------------------------------------

En production, Django ne sert pas nativement les fichiers statiques (CSS, JavaScript, images, polices de caractères). Le projet intègre **WhiteNoise**, une solution performante qui sert directement ces fichiers via l'application Python sans nécessiter de serveur web tiers (type Nginx ou Apache) :

* L'intergiciel ``whitenoise.middleware.WhiteNoiseMiddleware`` est positionné immédiatement après ``SecurityMiddleware``.
* Les fichiers sont compressés et mis en cache de manière optimale grâce au backend de stockage ``CompressedStaticFilesStorage``.
* Pendant l'exécution de la suite de tests, un basculement automatique vers ``StaticFilesStorage`` évite le besoin préalable d'un fichier manifeste précompilé.

Surveillance et traçabilité (Sentry & Logging)
----------------------------------------------

Surveillance proactive avec Sentry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Le SDK Sentry est initialisé au démarrage de Django à partir de la variable ``SENTRY_DSN``.
* Il intercepte automatiquement toute exception non gérée (erreur 500) et capture la pile d'exécution, l'environnement et le contexte de la requête HTTP.
* Lors de l'exécution des tests automatisés, Sentry est désactivé via le flag ``TESTING`` et la configuration ``conftest.py`` afin de préserver les quotas réseau.

Journalisation hiérarchisée (Logging)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* La configuration centralisée du dictionnaire ``LOGGING`` définit deux formateurs (``verbose`` et ``simple``) intégrant un horodatage précis (``datefmt: '%Y-%m-%d %H:%M:%S'``).
* Des loggers spécifiques sont configurés pour chaque application (``lettings``, ``profiles``, ``oc_lettings_site``).
* Niveaux de journalisation utilisés :
  - ``INFO`` : Suivi normal des requêtes et de la récupération des données.
  - ``WARNING`` : Tentatives d'accès à des ressources inexistantes (404).
  - ``ERROR`` : Exceptions inattendues accompagnées de la trace complète (``exc_info=True``).
