# Generated by Django 3.1.7 on 2021-04-24 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20210227_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date ajout'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='date_updated',
            field=models.DateTimeField(auto_now_add=True, verbose_name='derniere modification'),
        ),
    ]