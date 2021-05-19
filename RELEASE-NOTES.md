# En cours - "Extension du paramétrage"

### Nouvelles fonctionnalités
  * Ajout des types de publications à importer depuis HAL

### Corrections

### Améliorations

### Procédure de mise à jour

Mise à jour de la base avec:

 * python3 manage.py migrate
 * python3 manage.py init_publis

# V1.0.2 - 20 avril 2021 - "Participation des auteurs aux collections"

Extraction des informations donnant la participation des auteurs aux collections

### Nouvelles fonctionnalités
* Enregistrement dans la base des  participations
* Production du graphique montrant le réseau des co-publiants dans une collection 

### Corrections
 * Les titres passent en TextField pour éviter la limitation à 255 caractères

### Améliorations
 * Messages plus explicites

### Procédure de mise à jour

Mise à jour de la base avec:

 * python3 manage.py migrate

# V1.0.1 - 16 avril 2021 - "Ajout des fonctionnalités d'export"

Possibiité d'exporter images et graphiques

### Nouvelles fonctionnalités
* Les images sont téléchargeables directement de l'interface
* Images et bibtex d'une collection sont téléchargeables dsous forme de zip

### Corrections

### Améliorations

### Procédure de mise à jour
