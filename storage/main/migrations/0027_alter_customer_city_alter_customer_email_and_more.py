# Generated by Django 4.0.1 on 2022-04-23 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(default='', max_length=100, verbose_name='Ciudad'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(default='', max_length=10, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(default='', max_length=255, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(default='', max_length=255, verbose_name='Apellidos'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='number',
            field=models.CharField(default='', max_length=10, verbose_name='Numero'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='street',
            field=models.CharField(default='', max_length=100, verbose_name='Calle'),
        ),
    ]
