# focus_timer/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='user'
    )
# models.py
class Timers(models.Model):
    title = models.CharField(max_length=100)
    focus = models.IntegerField(default=25) # Focus time in minutes
    rest = models.IntegerField(default=5) # Rest time in minutes
    uuid = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    color = models.IntegerField(default=0) # 0-5 for each color profile