
   
############
Introduction
############

Ce système s'adresse aux institutions de recherche 
qui ont choisi Hal (https://hal.archives-ouvertes.fr/) 
pour déposer et gérer leurs publications scientifiques. HAL est très utile mais 
présente le double inconvénient de fournir d'une part une classification assez 
sommaire (soit, essentiellement, 'Article' et 'Communication'), 
et d'autre part d'être très permissif sur les données qui peuvent être déposées. 
Le risque est une incitation inflationiste au dépôt de publications de portée très variable, 
et une difficulté à identifier les publications les plus significatives.

Cristhal propose de clarifier le contenu d'un dépôt HAL en permettant de classer les publications 
selon des référentiels, qui peuvent être soit les référentiels internationaux comme SCIMAGO, 
soit des référentiels ad-hoc. 

L'architecture fonctionnelle est résumée par la :numref:`archiClassement`
Le système récupère les référentiels d'un côté (par import de fichiers CSV),  
les publications d'une collection HAL  de l'autre (via les services Web proposés par HAL) 
et effectue un appariement proposant une classification de chaque publication par 
rapport aux référentiels. Cette proposition doit être validée manuellement grâce à une interface dédiée. 
De nombreuses statistiques peuvent alors être produites.

.. _archiClassement:
.. figure:: ./figures/ArchiClassement.png       
        :width: 90%
        :align: center
   
        Vue d'ensemble de la procédure de classement des publications

Les fonctionnalités de CristHAL sont les suivantes

  - Configuration des collections HAL et import des référentiels fournis sous la forme de fichiers CSV
  - Récupération automatique des publications de chaque collection
  - Classement automatique suivi d'une validation manuelle
  - Production de graphiques et statistiques variées 
    (:numref:`stats-generales` et :numref:`stats_annee_classement`) sur les publications classées
  - Graphes de collaborations entre auteurs et entre collections (:numref:`reseau-coauteurs`)
  - Recherche des publications par formulaire ou par SQL
  - Export des figures en PDF ou PNG 
  - Exports en Latex, Bibtex ou CSV des données pour insertion dans des rapports et présentations

.. _stats-generales:
.. figure:: ./figures/stats-generales.png       
        :width: 90%
        :align: center
   
        Exemples de graphes statistiques produits par l'application

CristHAL est une application web écrite en Python/Django disponible sous forme de logiciel libre.
Elle a été initialement développée pour le laboratoire Cédric (http://cedric.cnam.fr) du Cnam
par Philippe Rigaux. 


.. _reseau-coauteurs:
.. figure:: ./figures/reseau-coauteurs.png       
        :width: 90%
        :align: center
   
        Réseau des co-auteurs au sein d'une collection

.. _stats_annee_classement:
.. figure:: ./figures/stats_annee_classement.png       
        :width: 90%
        :align: center
   
        Graphique montrant les classements des publications par année

Un environnement de test est disponible à http://cristhal.cnam.fr/. Demander un compte d'accès à philippe.rigaux@cnam.fr.
