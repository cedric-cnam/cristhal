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
    conférences invitées, etc.);
  - le classement "Valorisation" correspond aux logiciels et  brevets ;
  - le classement "National" correspond aux publications ayant une portée nationale;
  - seules les revues ou conférences internationales avec actes reçoivent un classement avec 
    quatre niveaux ; par analogie avec celui utilisé dans Scimago, ces quatre niveaux 
    sont dénommés Q1, Q2, Q3 et Q4;
  - enfin il existe un niveau "Hors référentiel", indiqué par le code "I", qui
    setrt de classement par défaut.
    
*À l'exception du code "Hors référentiel", il n'existe aucune interprétation de cette échelle dans CristHAL qui conditionnerait 
le fonctionnement du système*. Vous êtes donc tout à fait libres de la
conserver, de modifier les intitulés, ou de définir votre propre
échelle de classement.

.. important:: L'échelle doit être définie *avant* de commencer à classer les publications. Ensuite,
   il reste possible de changer les intitulés mais pas de supprimer un niveau de classement déjà utilisé.
   Enfin, c'est possible avec un peu de SQL direct, ce qu'il vaut mieux éviter...

Dans le menu d'administration, accédez à la fonction de gestion du classement des publications.
Vous obtenez l'interface de la :numref:`echelle_classement`.

.. _echelle_classement:
.. figure:: ./figures/echelle_classement.png       
        :width: 90%
        :align: center
   
        Administration de l'échelle de classement

Vous pouvez tout modifier librement *à l'exception du choix "Hors référentiel" que vous ne 
devez pas supprimer* (mais vous pouvez changer son intitulé). Encore une fois, il est 
fortement préférable de fixer l'échelle avant de commencer à classer.
 

***************************
Le formulaire de classement
***************************

Tout est prêt pour effectuer le classement des publications. À partir
du menu "Classement", choisissez une collection dans le menu local.
On obtient un formulaire dont un extrait est montré dans la :numref:`form-classement`.

.. _form-classement:
.. figure:: ./figures/form-classement.png       
        :width: 90%
        :align: center
   
        Le formulaire de classement

Le système propose, pour chaque publication, le classement le plus pertinent pour
chaque type de source. Ici, nous n'en avons que deux: CORE et SCIMAGO. 
Le classement de chaque source est affiché, selon sa propre codification.
On voit par exemple que la première publication de la 
:numref:`form-classement`, dans *Machine learning*, est classée A dans CORE, et 
Q1 dans SCIMAGO (ce qui est cohérent).


La dernière colonne permet de choisir le classement de la publication, 
avec un menu déroulant qui propose l'échelle de classement définie dans CristHAL.
Donc :

  - Vous devez définir une correspondance entre les classements des sources 
    et celui que vous souhaitez utiliser, et appliquer cette correspondance.
    Toujours dans le cas de la première publication ci-dessus, le classement
    Q1 est celui qui a été choisi en conformité avec les propositions issues des sources.
  - La correspondance entre la publication et la référence doit être claire. Si ce n'est pas le cas
    (exemple de la seconde publication),
    c'est soit que la publication est mal référencée dans HAL (et doit donc être corrigée car on
    souhaite  en principe que les publications Hal  soient référencées avec précision), soit que
    le référentiel est incomplet, soit enfin qu'elle
    doit être classée en hors référentiel.
  - Il se peut que le système ne propose que l'une des sources, si aucun appariement crédible
    n'a été proposé dans les autres.

Une fois le classement choisi dans le menu déroulant, vous pouvez cocher la case "Clasement
validé" pour indiquer que vous avez étudié et confirmé votre choix.

.. important:: À tout moment, et au plus tard avant de quitter la page, vous devez
   valider vos saisies avec le bouton "Valider" qui apparaît en haut du formulaire.
   
Il est toujours possible de changer les classements à tout moment.
