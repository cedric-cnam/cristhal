.. _chap-export:

##################
Export des données
##################

CristHAL fournit des fonctions d'export pour intégrer les données, graphiques
et statistiques à des rapports de recherches ou présentations. Ces exports se
font dans des fichiers placés dans le répertoire indiqué dans
la configuration, dont la valeur par défaut est ``/tmp``.
Vous pouvez changer ce paramétrage en vous assurant des droits d'accès.
Dans tous
les cas, le compte utilisateur qui exécute CritHAL doit avoir
des droits d'écriture.

Dans ce qui suit, ce répertoire est désigné par ``exportdir``.

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
    documents JSON dans le répertoire ``exportdir/<codeCol>/stats_publis/``
    (``<codeCol>`` est le code de la collection défini à la création).
  - Les fichiers Latex sont exportés dans ``exportdir/<codeCol>/docs_publis/``
  - Le répertoire ``exportdir/<codeCol>`` est ensuite zippé et le fichier Zip est téléchargé.

Avec la configuration par défaut et la collection  ``vertigo`` par 
exemple, l'export se fait dans ``/tmp/vertigo`` et le fichier retourné
par la fonction s'appelle ``vertigo.zip``. 

À partir des exports en JSON, on peut produire les formats graphiques
avec les outils Highcharts (https://www.highcharts.com/docs/export-module).
Il faut essentiellement installer le *Highcharts export server*, en fait 
un utilitaire Javascript, selon les instructions qui se trouvent
sur la page 
Github https://github.com/highcharts/node-export-server/blob/master/README.md.

Un fichier ``Makefile`` est copié dans ``exportdir/<codeCol>``. 
Si vous avez installé les outils précédents, 
la commande (sous un système de type Unix), exécutée dans le 
répertoire ``exportdir/<codeCol>``:

.. code-block:: bash

    make

produit les PDF  à partir des JSON. Il est très facile de produire d'autres 
formats.

*************************
Export des fichiers Latex
*************************

CristHAL exporte  dans ``exportdir/<codeCol>/docs_publis/`` 
des fichiers Latex. Le contenu de ces fichiers s'appuie sur le classement
et sur le type de publication. Actuellement nous avons

  - un tableau ``synthese_publis.tex`` donnant le nombre  de publications
    par type et par classement (figure :numref:`synthese-publis`)
  - des fichiers contenant des entrées ``bibitem`` 

Enfin,  dans ``exportdir/<codeCol>``, un fichier ``biblio_<codeCol>.tex``
est créé (par exemple ``biblio_vertigo.tex``). Il montre comment include les fichiers précédents dans un
rapport Latex contenant toute la bibliographie. On peut
le compiler directement avec ``pdflatex``.


.. _synthese-publis:
.. figure:: ./figures/synthese_publis.png       
        :width: 90%
        :align: center
   
        Tableau (après compilation Latex) de synthèse des publications

Il y a autant de fichiers Bibitem  que de type de publication et 
de classements (pour les types de publications sujettes à classement:
revues et conférences). Par exemple:

  - ``biblio_N1_ART.tex`` contient les bibitems des articles de revue 
    classés au niveau ``N1``.
  - ``biblio_N1_COMM.tex`` contient les bibitems des articles de conférence 
    classés au niveau ``N1``.
  - etc.
  
On peut ainsi choisir, dans un document Latex, quels niveaux de classement
on choisit de référencer.





