# Generated by Django 4.0.1 on 2022-04-18 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_order_order_finish'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='month',
            field=models.PositiveIntegerField(default=1, verbose_name='Meses'),
        ),
    ]
