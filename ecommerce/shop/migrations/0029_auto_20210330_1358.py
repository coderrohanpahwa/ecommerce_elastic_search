# Generated by Django 3.1.7 on 2021-03-30 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_orders_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='delivered',
            field=models.CharField(blank=True, choices=[('Yes', 'yes'), ('No', 'no')], default='No', max_length=10, null=True),
        ),
    ]
