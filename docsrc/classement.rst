.. _chap-classement:

###########################
Classement des publications
###########################

Le classement des publications s'effectue via une interface de saisie qui permet
de consulter et de valider l'appariement effectué par le moteur de recherche entre
les publications d'une collection et le référentiel. CristHAL n'effectue pas 
de classification entièrement automatique en raison des risques d'erreur (notamment
les publications saisies avec trop peu de précision, ou un référentiel incomplet).

Le classement s'effectue d'après une échelle qui est paramétrable.


***********************
L'échelle de classement
***********************

L'échelle de classement proposée par défaut est celle définie au laboratoire
Cédric. Elle comprend  7 catégories :
  
  - le classement "Communication" correspond aux exposés sans comité de lecture (séminaires,
    conférences invitées, etc.)
  - le classement "National" correspond aux publications ayant une portée nationale,
  - seules les revues ou conférences internationales avec actes reçoivent un classement avec 
    quatre niveaux ; par analogie avec celui utilisé dans Scimago, ces quatre niveaux 
    sont dénommés Q1, Q2, Q3 et Q4.
  - enfin il existe un niveau "Hors référentiel", indiqué par le code "I", qui
    setrt de classement par défaut.
    
*À l'exception du code "Hors référentiel", il n'existe aucune interprétation de cette échelle dans CristHAL qui conditionnerait 
le fonctionnement du système*. Vous êtes donc tout à fait libres de la
conserver, de modifier les intitulés, ou de définir votre propre
échelle de classement.

.. important:: L'échelle doit être définie *avant* de commencer à classer les publications. Ensuite,
   il reste possible de changer les intitulés mais pas de supprimer un nievau classement déjà utilisé.
   Enfin, c'est possible avec un peu de SQL direct, ce qu'il vaut mieux éviter...


***************************
Le formulaire de classement
***************************


