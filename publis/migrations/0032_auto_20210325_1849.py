# Generated by Django 2.2.18 on 2021-03-25 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publis', '0031_collection_id_hal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auteur',
            old_name='nom',
            new_name='nom_complet',
        ),
        migrations.RemoveField(
            model_name='auteur',
            name='prenom',
        ),
        migrations.AlterField(
            model_name='auteur',
            name='idHal',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
