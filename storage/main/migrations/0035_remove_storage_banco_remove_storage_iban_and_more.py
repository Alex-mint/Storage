# Generated by Django 4.0.1 on 2022-05-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_order_payment_intent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='banco',
        ),
        migrations.RemoveField(
            model_name='storage',
            name='iban',
        ),
        migrations.AddField(
            model_name='storage',
            name='public_key',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Clave publico'),
        ),
        migrations.AddField(
            model_name='storage',
            name='secret_key',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Plave privado'),
        ),
    ]
