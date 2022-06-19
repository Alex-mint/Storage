# Generated by Django 4.0.1 on 2022-04-11 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_address', to='main.customeraddress', verbose_name='Direccion'),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Numero'),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefono'),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='street',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Calle'),
        ),
    ]