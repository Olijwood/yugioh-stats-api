from django.db import models

# Create your models here.
class Game(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    display_name = models.CharField(max_length=200)