# Generated by Django 4.0.10 on 2024-05-15 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=12, null=True)),
                ('average_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SetScrapeRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
