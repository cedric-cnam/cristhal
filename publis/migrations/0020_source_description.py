# Generated by Django 2.2.13 on 2021-01-15 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publis', '0019_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='description',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
