# Generated by Django 3.1.7 on 2021-03-25 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20210325_1733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory',
            old_name='catgeory',
            new_name='category',
        ),
    ]