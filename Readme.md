# Un système de classement des publications HAL

Ce système s'adresse aux institutions de recherche qui ont choisi [Hal](https://hal.archives-ouvertes.fr/) pour déposer et gérer leurs publications
scientifiques. HAL est très utile mais présente le double inconvénient de fournir d'une part une classification assez sommaire (soit, essentiellement, 'Article'  et 'Communication'), et d'autre part d'être très permissif sur les données qui peuvent être déposées. Le risque est une incitation inflationiste au dépôt de publications de portée très variable, et difficulté à identifier les publications les plus significatives.
<p align="center">
<img src="/docsrc/figures/ArchiClassement.png" width="700"> 
  </p>

L’architecture fonctionnelle est résumée par la figure ci-dessus.
Cristhal propose de clarifier le contenu d'un dépôt HAL en permettant de classer les publications selon des référentiels, qui peuvent être soit les référentiels internationaux comme [SCIMAGO](https://www.scimagojr.com/), soit des référentiels ad-hoc. Le système récupère les publications d'une collection HAL d'un côté, les référentiels de l'autre, et effectue un appariement proposant une classification de chaque publication par rapport aux référentiels. Cette proposition doit être validée manuellement. De nombreuses statistiques peuvent alors être produites. 

Les fonctionnalités sont les suivantes
  - Configuration des collections HAL et import des référentiels fournis sous la forme de fichiers CSV
  - Récupération automatique des publications de chaque collection
  - Classement automatique suivi d'une validation manuelle
  - Production de graphiques et statistiques variées (cf. exemples ci-dessous)sur les publications classées
  - Graphes de collaborations entre auteurs et entre collections
  - Recherche des publications par formulaire ou par SQL
  - Export des figures en PDF ou PNG 
  - Exports en Latex, Bibtex ou CSV des données pour insertion dans des rapports et présentations

Les statistiques sont produites sous forme de graphiques exportables:

<p align="center">
<img src="/docsrc/figures/stats-generales.png" width="600"> 
</p>

Les classements sont à la base de graphiques qui analysent l'évolution des publications.

<p align="center">
<img src="/docsrc/figures/stats_annee_classement.png" width="700"> 
</p>
CristHAL est une application web Python/Django disponible en libre accès, initialement développée pour le laboratoire 
[Cédric](https://cedric.cnam.fr) du Cnam par Philippe Rigaux. Toutes les informations pour l'installer et l'utiliser se trouvent dans la 
[documentation en ligne](https://cedric-cnam.github.io/cristhal/).

Un environnement de test est disponible à http://cristhal.cnam.fr/. Demander un compte d'accès à philippe.rigaux@cnam.fr.

