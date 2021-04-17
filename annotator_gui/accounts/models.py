from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    Phone = models.IntegerField(blank = True, null = True)
    AssignedPatients = models.TextField(blank = True, null = True, default='None')
    Keywords = models.TextField(blank = True, null = True, default='dementia')
    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username
