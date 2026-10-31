Base de données et modèles de données
======================================

Schéma global de données
------------------------

L'application repose sur trois modèles de données principaux, répartis selon leurs responsabilités métier :

1. ``Address`` (application ``lettings``) : Représente une adresse physique.
2. ``Letting`` (application ``lettings``) : Représente une offre d'hébergement locatif liée à une adresse.
3. ``Profile`` (application ``profiles``) : Représente un profil utilisateur étendu relié au compte d'authentification natif de Django (``django.contrib.auth.models.User``).

Diagramme relationnel
---------------------

.. code-block:: text

   +------------------------------------+
   |               User                 |
   |   (django.contrib.auth.models)     |
   +------------------------------------+
   | id          : AutoField (PK)       |
   | username    : CharField(150)       |
   | first_name  : CharField(150)       |
   | last_name   : CharField(150)       |
   | email       : EmailField           |
   +-----------------+------------------+
                     | 1
                     |
                     | 1
   +-----------------v------------------+
   |              Profile               |
   |        (profiles.models)           |
   +------------------------------------+
   | id            : AutoField (PK)     |
   | user_id       : OneToOneField      |
   | favorite_city : CharField(64)      |
   +------------------------------------+

   +------------------------------------+       +------------------------------------+
   |              Address               |       |              Letting               |
   |         (lettings.models)          |       |         (lettings.models)          |
   +------------------------------------+       +------------------------------------+
   | id               : AutoField (PK)  | 1   1 | id         : AutoField (PK)        |
   | number           : PositiveInt     <-------+ address_id : OneToOneField         |
   | street           : CharField(64)   |       | title      : CharField(256)        |
   | city             : CharField(64)   |       +------------------------------------+
   | state            : CharField(2)    |
   | zip_code         : PositiveInt     |
   | country_iso_code : CharField(3)    |
   +------------------------------------+

Détail des modèles
------------------

Modèle ``Address`` (Application ``lettings``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enregistre la localisation géographique détaillée d'un bien locatif.

.. autoclass:: lettings.models.Address
   :show-inheritance:

Champs du modèle :

* ``number`` (``PositiveIntegerField``) : Numéro dans la rue (limité à la valeur maximale 9999).
* ``street`` (``CharField``, max 64) : Nom de la rue ou voie.
* ``city`` (``CharField``, max 64) : Ville.
* ``state`` (``CharField``, 2 caractères) : Code de l'État (ex. : ``CA`` pour la Californie).
* ``zip_code`` (``PositiveIntegerField``) : Code postal (valeur maximale 99999).
* ``country_iso_code`` (``CharField``, 3 caractères) : Code ISO pays à 3 lettres (ex. : ``USA``).

Modèle ``Letting`` (Application ``lettings``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Représente l'annonce de location de vacances.

.. autoclass:: lettings.models.Letting
   :show-inheritance:

Champs du modèle :

* ``title`` (``CharField``, max 256) : Titre de l'annonce de location.
* ``address`` (``OneToOneField`` vers ``Address``) : Relation biunivoque stricte avec une adresse physique.

Modèle ``Profile`` (Application ``profiles``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Étend les données associées à un utilisateur standard de Django.

.. autoclass:: profiles.models.Profile
   :show-inheritance:

Champs du modèle :

* ``user`` (``OneToOneField`` vers ``django.contrib.auth.models.User``) : Lien avec le compte d'authentification.
* ``favorite_city`` (``CharField``, max 64, optionnel) : Ville favorite renseignée par l'utilisateur.

Stratégie de migration des données
-----------------------------------

Lors de la transition de l'ancienne architecture monolithique vers la nouvelle architecture modulaire :

1. Les tables initiales ``oc_lettings_site_address``, ``oc_lettings_site_letting`` et ``oc_lettings_site_profile`` contenaient les données d'origine.
2. Les migrations initiales (``0001_initial``) ont créé les nouvelles tables ``lettings_address``, ``lettings_letting`` et ``profiles_profile``.
3. Des migrations de données personnalisées (``0002_copy_data``) ont transféré l'ensemble des enregistrements existants de manière fiable sans aucune perte d'intégrité ni de clés étrangères.
4. Enfin, une migration de nettoyage dans ``oc_lettings_site`` a supprimé en toute sécurité les anciens modèles obsolètes.
