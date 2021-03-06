# Generated by Django 3.1.7 on 2021-04-18 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publis', '0003_auto_20210411_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participation', to='publis.auteur')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participation', to='publis.collection')),
            ],
            options={
                'db_table': 'Participation',
            },
        ),
        migrations.AddField(
            model_name='collection',
            name='auteurs',
            field=models.ManyToManyField(blank=True, related_name='collections', through='publis.Participation', to='publis.Auteur'),
        ),
    ]
