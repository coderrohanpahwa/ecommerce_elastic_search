# Generated by Django 3.1.7 on 2021-03-27 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20210327_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='addtocart',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.buyer'),
        ),
    ]
