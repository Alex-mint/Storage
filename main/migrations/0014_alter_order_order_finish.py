# Generated by Django 4.0.1 on 2022-04-18 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_order_order_date_order_order_finish_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_finish',
            field=models.DateField(verbose_name='Fin de pedido'),
        ),
    ]
