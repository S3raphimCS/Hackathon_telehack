# Generated by Django 4.2.7 on 2023-11-11 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='report',
            name='region',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Регион'),
        ),
    ]
