# Generated by Django 3.1.7 on 2021-03-26 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20210326_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='quality_type',
            field=models.CharField(choices=[('Premium', 'Premium'), ('High', 'High'), ('Low', 'Low'), ('Bad', 'Bad')], max_length=20),
        ),
    ]
