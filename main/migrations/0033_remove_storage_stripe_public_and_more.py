# Generated by Django 4.0.1 on 2022-04-29 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_remove_storage_iban_storage_stripe_public_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='stripe_public',
        ),
        migrations.RemoveField(
            model_name='storage',
            name='stripe_secret',
        ),
        migrations.AddField(
            model_name='storage',
            name='iban',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Iban'),
        ),
    ]
