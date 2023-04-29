from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_CustomerAssistant = models.BooleanField('Is Customer Assistant',default=False)
    is_Manager = models.BooleanField('Is Manager',default=False)
    is_StoreManager = models.BooleanField('Is Store Manager',default=False)
    