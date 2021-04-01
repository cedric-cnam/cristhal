# Generated by Django 2.2.13 on 2021-01-13 22:33

from django.db import migrations


def ajout_classement_publi (apps, schema_editor):
    '''
      Ajout d'un niveau par défaut aux codes de classement publi
    '''
    ClassementPubli = apps.get_model('publis', 'ClassementPubli')
    classement_defaut = ClassementPubli(code='I', libelle='Indéterminé')
    classement_defaut.save()



class Migration(migrations.Migration):

    dependencies = [
        ('publis', '0016_classementpubli'),
    ]

    operations = [
        migrations.RunPython(ajout_classement_publi),
    ]
