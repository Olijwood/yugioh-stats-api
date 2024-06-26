# Generated by Django 4.0.10 on 2024-05-22 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sets', '0003_usersubmittedsetpricestats'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubmittedSetPrices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_title', models.CharField(max_length=200)),
                ('simulated_price', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.RemoveField(
            model_name='usersubmittedsetpricestats',
            name='set_title',
        ),
        migrations.RemoveField(
            model_name='usersubmittedsetpricestats',
            name='simulated_price',
        ),
        migrations.AddField(
            model_name='usersubmittedsetpricestats',
            name='booster_mean',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usersubmittedsetpricestats',
            name='booster_median',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usersubmittedsetpricestats',
            name='chance_greater_opened_value',
            field=models.FloatField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='usersubmittedsetpricestats',
            name='date_submitted',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usersubmittedsetpricestats',
            name='set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sets.set'),
        ),
    ]
