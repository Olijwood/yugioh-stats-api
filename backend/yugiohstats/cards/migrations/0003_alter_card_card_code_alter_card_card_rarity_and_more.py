# Generated by Django 4.0.10 on 2024-05-21 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_pricehistory_cardimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_rarity',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='tcg_num_listings',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
