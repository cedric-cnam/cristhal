# Generated by Django 2.2.13 on 2021-01-15 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publis', '0018_auto_20210113_2240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier', models.FileField(upload_to='')),
                ('pref_ref', models.CharField(max_length=10, unique=True)),
                ('a_charger', models.BooleanField()),
            ],
            options={
                'db_table': 'Source',
            },
        ),
    ]
