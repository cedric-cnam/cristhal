.. _chap-referentiel:

######################
Gestion du référentiel
######################

Le référentiel est un ensemble de revues  ou de conférences scientifiques, chacune associée à un
ou plusieurs classement fournis par des *sources*. Le principe de CristHAL est de permettre d'adosser
toute publication à une référence issue d'une source reconnue, internationalement ou nationalement. Mais
il est également possible de fournir un classement *ad-hoc*, à partir d'une source
dite "interne".

La gestion du référentiel consiste à ajouter des sources, à les charger, et à chercher ensuite, pour chaque
publication, la référence la plus proche.

***********************
Définition d'une source
***********************

Les sources sont fournies sous la forme de fichiers CSV. Selon la source, le format peut varier, et CristHAL
propose donc un ensemble de fonctions d'import adaptée à chaque type de source. 

Chaque fichier CSV doit contenir une première ligne qui indique la fonction de chqaue champ. Parmi
ces champs, il faut au moins:

  - l'identifiant interne à la source
  - le titre de la revue ou conférence 
  - le classement, selon une codification propre à la source

Voici les formats que quelques sources.

Scimago
=======

Le site https://www.scimagojr.com/journalrank.php propose une classification de revues scientifiques
dans de très nombreux domaines et sous-domaines. Pour chacun il est possible d'exporter
en CSV la liste des références. Ce fichier contient une ligne d'entête et peut
directement être importé dans CristHAL.

Dans le répertoire ``cristhaldir/install``, vous trouverez quelques exemples d'exports CSV Scimago.


CORE
====

Une association scientifique australienne (http://portal.core.edu.au/) propose une classification des revues
et des conférences dans le domaine de la science informatique. Les fichiers CSV ne contiennent pas de première
ligne descriptive qui doit donc être ajoutée. Pour les conférences, cette ligne est la suivante:

.. code-block:: text
  
     ID,Titre,Acronyme,source,Classement,dblp,hasData,domaine,commentaires,notes
     
Pour les revues:

.. code-block:: text

     ID,Titre,source,Classement,dblp,hasData,domaine,domaine2,domaine3

Dans le répertoire ``cristhaldir/install``, vous trouverez les fichiers CORE 2020.

Classements internes
====================

Une source dite *interne*  permet à une institution de définir son propre classement.
Il peut être destiné à compléter les référentiels internationaux, par exemple pour
indiquer les classements de niveau national  ou les communications dans
des conférences non référencées dans les sources existantes.

Il peut également servir à corriger les classements de référence. Enfin, il peut également
servir à attribuer un classement Cédric (Q1, Q2, Q3 ou Q4) dans le cas où des revues ou conférences
nationale à comités de lecture ont en fait une portée internationale qui le justifie. 

Le fichier CSV doit contenir au moins les champs ID, Titre, Classement et Type (dont l'emplacement
est défini par la première ligne d'entête. Voici un exemple du format attendu:

..  code-block:: text

    ID;Acronyme;Titre;Classement;Type
    vertigo1;BDA;Conférence sur la Gestion de Données Principes, Technologies et Applications - Bases de données avancées;National;COMM
    vertigo2;ISMIR;International Symposium on Music Information Retrieval;Q2;COMM

Pour produire un fichier source CSV importable dans CristHAL, le plus simple est d'utiliser un tableur.
Dans ``cristhaldir/install``, vous trouverez le fichier que nous utilisons au laboratoire Cédric
(en le partageant dans un environnement collaboratif). Il contient la codification utilisée
au Cédric, et un onglet par équipe. Chaque onglet peut être exporté en CSV avec Excel, OpenOffice
ou Numbers.

Autres classements
==================

Il est facile d'ajouter d'autres types de sources. Soit en changeant la première ligne pour indiquer
les positions des champs importants, soit en demandant une extension de CristHAL.

*********************
Création d'une source
*********************

Dans le menu d'administration, accéder au choix 'Sources' et au formulaire de création (:numref:`form-source`).

.. _form-source:
.. figure:: ./figures/form-source.png       
        :width: 90%
        :align: center
   
        Formulaire de saisie / mise à jour des sources

Les données à saisir:

  - le fichier CSV de la source
  - une description
  - l'identifiant de la source (unique) ; en combinant cet identifiant et celui, interne, de
    chaque référence de la source, on obtient l'identifiant unique d'une référence au sein du référentiel
  - le délimiteur des champs dans le fichier CSV (en général, le point-virgule, les fichiers CORE étant une exception)
  - le type de la source

Pour l'identifant des sources, utiliser une courte chaîne de caractères, 
par exemple ``core_revue``,
``interne_optim``, ....

La figure ci-dessous montre la saisie de la source contenant les
revues de mathématiques de SCIMAGO. Le fichier est ``SCIMAGO-MATHS.csv``
dans ``cristhal/install``.

.. _saisie-source:
.. figure:: ./figures/saisie-source.png       
        :width: 90%
        :align: center
   
        Exemple de saisie d'une source SCIMAGO Maths dans le référentiel



Il reste à charger ou recharger une source pour l'indexer.  Dans le menu ``Référentiel``, la liste
des sources apparaît, avec une option ``charger`` ou ``recharger``.  


.. _page-referentiel:
.. figure:: ./figures/page-referentiel.png       
        :width: 90%
        :align: center
   
        La page du référentiel

Le nombre de références d'une source est donné entre parenthèses après chargement
(:numref:`page-referentiel`, après chargement d'un fichier CORE).


****************************
Interrogation du référentiel
****************************

La fonction "Recherche dans le référentiel" permet d'effectuer directement une recherche par mots-clés
et d'obtenir une liste classée par pertinence descendante des 10 premières références correspondant
aux mots-clés (:numref:`recherche_ref`).

.. _recherche_ref:
.. figure:: ./figures/recherche_ref.png       
        :width: 90%
        :align: center
   
        Formulaire de recherche dans le référentiel

C'est la même fonction qui sera appelée au moment du classement avec, en lieu
et place des mots-clés, le titre de la revue ou le nom de la conférence. La
procédure de classement proposera alors, pour
chaque publication, les meilleures références possibles. 

En utilisant directement le formulaire de recherche, on peut donc contrôler la présence
dans le référentiel de revues ou de conférences, et vérifier que le classement
par pertinence est correct. 

La recherche fonctionne selon les principes classiques de la Recherche d'Information (RI)
pour des collections de documents textuels. L'ordre des mots-clés est
indifférent, chaque mot est soumis à différentes transformations et simplifications, et 
le moteur détermine un classement basé sur la similarité entre les mots-clés et le 
texte des références. 

Les deux principales causes d'un mauvais classement sont:

  - Une saisie incorrecte ou incomplète du titre de la revue ou du nom de la conférence
    dans la publication ; il n'y a pas alors de meilleure solution que de corriger 
    dans HAL et de recharger la collection.
  - L'absence de la conférence ou de la revue dans le référentiel. On peut choisir 
    de l'ajouter, ou considérer que la publication est "Hors référentiel".

Hors ces deux causes, le moteur de recherche devrait toujours être en mesure de trouver la meilleure solution.

