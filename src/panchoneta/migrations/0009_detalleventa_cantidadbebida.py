# Generated by Django 5.2.3 on 2025-06-24 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panchoneta', '0008_alter_detalleventa_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleventa',
            name='cantidadBebida',
            field=models.BigIntegerField(blank=True, help_text='cantidad bebidas', null=True, verbose_name='cantidad'),
        ),
    ]
