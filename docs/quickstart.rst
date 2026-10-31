Démarrage rapide et guide d'utilisation
========================================

Lancement du serveur de développement
-------------------------------------

Pour démarrer le serveur de développement local de Django, exécutez la commande suivante à la racine du projet :

.. code-block:: bash

   python manage.py runserver

Le serveur sera alors accessible à l'adresse suivante : `http://127.0.0.1:8000/ <http://127.0.0.1:8000/>`_.

Parcours des fonctionnalités
----------------------------

Page d'accueil
~~~~~~~~~~~~~~
* **URL** : ``/``
* **Description** : Présente l'interface principale de *Orange County Lettings* avec des liens directs vers les sections **Profiles** et **Lettings**.
* **Pied de page (UI)** : Affiche la date et l'heure courante du serveur pour corréler facilement les interactions visuelles avec les journaux d'événements (logs).

Section Locations (*Lettings*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* **Liste des locations** : ``/lettings/``
  Affiche la liste complète des biens immobiliers disponibles à la location.
* **Détail d'une location** : ``/lettings/<letting_id>/`` (par exemple ``/lettings/1/``)
  Affiche le titre de la location ainsi que son adresse complète (numéro, rue, ville, code postal, État et code pays).
  Si l'identifiant demandé n'existe pas en base de données, l'application capture l'exception ``Letting.DoesNotExist`` et renvoie la page d'erreur personnalisée 404.

Section Profils (*Profiles*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* **Liste des profils** : ``/profiles/``
  Affiche la liste de tous les utilisateurs enregistrés sur le site.
* **Détail d'un profil** : ``/profiles/<username>/`` (par exemple ``/profiles/HeadlinesGazer/``)
  Affiche les détails du compte utilisateur : nom d'utilisateur, prénom, nom, adresse e-mail et ville favorite.
  Si le nom d'utilisateur n'existe pas, l'application capture ``Profile.DoesNotExist`` et renvoie la page 404.

Interface d'administration Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* **URL** : ``/admin/``
* **Description** : Permet aux administrateurs de créer, modifier et supprimer des locations, des adresses et des profils utilisateurs.
* Pour créer un compte administrateur local :

  .. code-block:: bash

     python manage.py createsuperuser

Vérification de la surveillance Sentry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* **URL** : ``/sentry-debug/``
* **Description** : Cette route déclenche intentionnellement une exception ``ZeroDivisionError`` (division par zéro).
* Elle permet de vérifier que le SDK Sentry intercepte correctement les erreurs inattendues et les transmet en direct au tableau de bord Sentry associé au DSN configuré.

Gestion des erreurs HTTP
~~~~~~~~~~~~~~~~~~~~~~~~
* **Erreur 404 (Page non trouvée)** : Visiter une URL inexistante (ex. : ``/page-introuvable/``) affiche un modèle graphique épuré et compréhensible pour l'utilisateur, tout en consignant l'URL demandée dans les logs de niveau WARNING.
* **Erreur 500 (Erreur interne du serveur)** : Si une exception non interceptée survient lors du traitement d'une requête, Django renvoie une page d'erreur 500 personnalisée et consigne la trace complète de l'exception (``exc_info=True``) dans les logs d'erreurs.
