# Generated by Django 4.0.10 on 2024-06-03 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sets', '0019_setrankings_ranking_change'),
    ]

    operations = [
        migrations.RenameField(
            model_name='setrankings',
            old_name='ranking_change',
            new_name='ml_ranking_change',
        ),
        migrations.AddField(
            model_name='setrankings',
            name='mp_ranking_change',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
