# Generated by Django 3.1.7 on 2021-03-27 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20210327_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]