# Generated by Django 4.0.1 on 2022-04-19 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_item_storage'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='main',
            field=models.BooleanField(default=False, verbose_name='Principal'),
        ),
    ]
