# Generated by Django 3.1.5 on 2021-01-09 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='civility',
            field=models.CharField(choices=[('Mr', 'Mr'), ('Mme', 'Mme'), ('Mlle', 'Mlle')], default='Mr', max_length=4, verbose_name='civilité'),
        ),
        migrations.DeleteModel(
            name='Tagulous_User_civility',
        ),
    ]