# Generated by Django 4.0.1 on 2022-05-06 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_remove_storage_stripe_public_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_intent',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Id de transferencia'),
        ),
    ]
