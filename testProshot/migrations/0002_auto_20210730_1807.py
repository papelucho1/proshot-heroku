# Generated by Django 3.2 on 2021-07-31 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testProshot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='cantidadDePreguntas',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='test',
            name='isAvailable',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
