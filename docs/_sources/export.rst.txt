.. _chap-export:

##################
Export des données
##################

CristHAL fournit des fonctions d'export pour intégrer les données, graphiques
et statistiques à des rapports de recherches ou présentations. Ces exports se
font dans des fichiers placés dans le répertoire ``EXPORT_DIR`` 
qui est, dans la configuration par défaut, un sous-répertoire de ``media``
nommé ``export``.

.. code-block:: python

    EXPORT_DIR = os.path.join(MEDIA_ROOT, 'export')

Vous pouvez changer ce paramétrage en vous assurant des droits d'accès.
CristHAL tente de créer le répertoire ``export`` s'il n'existe pas. Dans tous
les cas, le compte utilisateur qui exécute CritHAL doit avoir
des droits d'écriture.

Dans ce qui suit, ce répartoire est désigné par ``exportdir``.

*********************
Export des graphiques
*********************

.. important:: Si vous souhaitez exporter un seul graphique, utilisez 
   le menu local en haut à droite, comme illustré sur la :numref:`menu_local_export`

.. _menu_local_export:
.. figure:: ./figures/menu_local_export.png       
        :width: 90%
        :align: center
   
        Menu local d'export des images
        
Les exports se font par collection, à l'aide du choix ``export``  dans le
tableau de la page d'accueil. 

  - Les graphiques sont exportés sous forme de 
    documents JSON dans le répertoire ``exportdir/<codeCol>/<nomGraphique>``
    (``<codeCol>`` est le code de la collection défini à la création).
  - Ce répertoire est ensuite zippé et le fichier Zip est téléchargé.

À partir des exports en JSON, on peut produire les formats graphiques
avec les outils Highcharts (https://www.highcharts.com/docs/export-module).
Il faut essentiellement installer le *Highcharts export server*, en fait 
un utilitaire Javascript, selon les instructions qui se trouve
sur la page 
Github https://github.com/highcharts/node-export-server/blob/master/README.md.

Un fichier ``Makefile`` est fourni à titre d'exemple pour dans
le répertoire ``cristhaldir/install``. En plaçant ce fichier dans
le répertoire d'export et en entrant la commande (sous un système de type Unix):

.. code-block:: bash

    make

Les PDF sont produits à partir des JSON. Il est très facile de produire d'autres 
formats.


*****************
Export des bibtex
*****************

CritHAL exporte des fichiers ``.bib`` contenant les entrées Bibtex des
publications de la collection exportée. Ces entrées sont celles produites
par HAL.


.. note:: À l'avenir il est possible que d'autres modèles Bbtex soient proposés.

Il y a autant de fichiers ``.bib`` que de catégories dans le classement 
des publications. Chaque fichier est suffixé par le code du classement:
on peut ainsi choisir, dans un document Latex, quels niveaux de classement
on choisit de référencer.





