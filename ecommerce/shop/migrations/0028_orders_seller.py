# Generated by Django 3.1.7 on 2021-03-30 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_sellerincome'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.seller'),
        ),
    ]
