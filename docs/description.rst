Description du projet
=====================

Présentation générale
---------------------

**Orange County Lettings** est une plateforme web de réservation et de consultation de résidences de vacances. L'application permet aux utilisateurs de parcourir un catalogue d'hébergements de vacances (locations), d'en consulter les adresses et détails précis, ainsi que d'accéder aux profils utilisateurs enregistrés sur la plateforme.

Contexte de la refonte
----------------------

Le projet initial souffrait d'une architecture monolithique dans laquelle l'ensemble des modèles, vues et logiques métier étaient regroupés au sein d'une unique application Django centrale (``oc_lettings_site``). Cette structure présentait plusieurs limites :

* Fort couplage entre des domaines métier distincts (gestion des biens en location d'un côté, gestion des profils utilisateurs de l'autre).
* Difficulté à faire évoluer et tester chaque domaine de manière isolée.
* Absence de monitoring d'erreurs en production et traçabilité insuffisante.
* Absence d'automatisation des tests et du déploiement.

Objectifs de la modernisation
-----------------------------

Dans le cadre du Projet 13 du parcours Développeur d'application Python d'OpenClassrooms, l'application a été profondément remaniée pour répondre aux standards de l'ingénierie logicielle moderne :

1. **Architecture modulaire** : Découpage du projet en applications autonomes à forte cohésion et faible couplage (``lettings`` et ``profiles``).
2. **Réduction de la dette technique** :
   - Conformité totale avec les normes PEP 8 via Flake8.
   - Documentation de chaque fonction, classe et module par des docstrings explicites.
   - Suite complète de 25 tests automatisés avec Pytest.
   - Couverture de test maintenue au-dessus de 90 % (seuil minimal imposé : 80 %).
   - Pages d'erreur 404 et 500 personnalisées.
3. **Surveillance et traçabilité** :
   - Intégration de Sentry pour la détection et la capture en temps réel des exceptions.
   - Configuration de logs hiérarchisés avec horodatage précis (date et heure).
   - Sécurisation des secrets applicatifs via des variables d'environnement.
4. **Conteneurisation et CI/CD** :
   - Image Docker légère et optimisée pour la production.
   - Pipeline d'intégration et de déploiement continu automatisé avec GitHub Actions.
   - Déploiement automatique sur le service cloud Render.
5. **Documentation technique complète** :
   - Génération automatisée avec Sphinx et publication sur Read The Docs.
