# Generated by Django 2.2.13 on 2021-01-09 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publis', '0008_referentiel_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='referentiel',
            name='ref_locale',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
