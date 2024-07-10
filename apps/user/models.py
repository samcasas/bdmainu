from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    NEW = 0
    ACTIVE = 1
    INACTIVE = 2
    DELETED = 3

    STATUS_CHOICES = [
        (NEW, 'New'),
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (DELETED, 'Deleted'),
    ]
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW)

    class Meta:
        abstract = True

class User(BaseModel):
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    password = models.CharField(max_length=128)
    restaurant_id = models.CharField(max_length=500, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)  
    tokenExpirationDate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
#class Restaurant(BaseModel):
#    logo = models.CharField(max_length=500)
#    description = models.TextField(blank=True, null=True)

#class Menu(models.Model):
#    logo = models.CharField(max_length=500)
#    description = models.TextField(blank=True, null=True)

    
