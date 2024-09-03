from django.db import models

class BaseModel(models.Model):
    ACTIVE = 1
    INACTIVE = 0

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        abstract = True
class Category(BaseModel):
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(blank=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.name}'

class Product(BaseModel):
    category_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.name} - {self.price}'

class Promotion(BaseModel):
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(blank=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.name}'
    