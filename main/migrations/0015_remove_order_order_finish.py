# Generated by Django 4.0.1 on 2022-04-18 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_order_order_finish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_finish',
        ),
    ]