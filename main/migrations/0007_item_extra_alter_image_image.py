# Generated by Django 4.0.1 on 2022-04-16 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='extra',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='Fotos de pedido'),
        ),
    ]
