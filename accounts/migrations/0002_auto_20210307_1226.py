# Generated by Django 3.1.7 on 2021-03-07 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customer',
            new_name='GuestCustomer',
        ),
    ]
