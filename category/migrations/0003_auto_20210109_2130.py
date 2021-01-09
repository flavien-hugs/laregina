# Generated by Django 3.1.5 on 2021-01-09 21:30

from django.db import migrations
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_auto_20210109_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='keywords',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, blank=True, help_text='Enter a comma-separated tag string', to='category.Tagulous_Category_keywords', verbose_name='mot clés'),
        ),
    ]
