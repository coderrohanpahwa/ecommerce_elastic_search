# Generated by Django 3.1.7 on 2021-03-27 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_orders_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='delivered',
            field=models.CharField(blank=True, choices=[('Yes', 'yes'), ('No', 'no')], max_length=10, null=True),
        ),
    ]