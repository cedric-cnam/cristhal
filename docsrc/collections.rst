.. _chap-collections:

#######################
Gestion des collections
#######################

CristHAL récupère pour les analyser des collections de publications appartenant à une *structure*
HAL. Chaque structure a un nom (par exemple CEDRIC-VERTIGO pour l'équipe VERTIGO du Cédric) 
et un identifiant (par exemple 553459 pour cette même équipe). Le 
lien https://aurehal.archives-ouvertes.fr/structure/browse?critere=cedric&category=*
donne par exemple la liste des structures (équipes en l'occurrence) du laboratoire
Cédric.


.. note:: Reportez-vous à la documentation https://doc.archives-ouvertes.fr/gerer-un-portail/referentiels/structures-de-recherche/ 
          pour des informations sur la notion de structure de recherche dans HAL.

Pour demander l'analyse des publications d'une structure dans CristHAL, vous devez
d'avord la définir, puis la synchroniser avec HAL.

.. important:: L'ensemble des publications d'une structure est une *collection* dans CristHAL.

***************************
Définition d'une collection
***************************





.. _archiTechue:
.. figure:: ./figures/ArchiTechnique.png       
        :width: 90%
        :align: center
   
        Les composants techniques

