# Generated by Django 4.1.1 on 2022-10-07 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Избранное'),
        ),
    ]
