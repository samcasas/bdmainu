from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
class BaseModel(models.Model):
    NEW = 0
    ACTIVE = 1
    INACTIVE = 2
    DELETED = 3
    TOUR = 4

    STATUS_CHOICES = [
        (NEW, 'New'),
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (DELETED, 'Deleted'),
        (TOUR, 'Tour'),
    ]
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW)

    class Meta:
        abstract = True

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500, unique=True)
    password = models.CharField(max_length=128)
    phone = models.IntegerField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    restaurant_id = models.CharField(max_length=500, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)
    tokenExpirationDate = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    def __str__(self):
        return f"{self.id} - {self.email} - {self.name}"

    
