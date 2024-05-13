import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Фотография')
    email = models.EmailField(unique=True, blank=False)
    date_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    is_confirmed = models.BooleanField(default=False)


# --------------------------------------- Email class ---------------------------------------------------
class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

# --------------------------------------- Email class ---------------------------------------------------
