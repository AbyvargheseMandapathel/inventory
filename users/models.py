from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'
    MANAGER = 'manager'
    STAFF = 'staff'
    USER='user'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (STAFF, 'Staff'),
        (USER,'User'), 

    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)


# Create your models here.


