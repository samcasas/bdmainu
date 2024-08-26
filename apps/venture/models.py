from django.db import models

class Venture(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

class Branch(models.Model):
    venture_id = models.IntegerField()
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    external_number = models.IntegerField()
    internal_number = models.IntegerField(blank=True, null=True)
    cp = models.CharField(max_length=10)  
    suburb = models.CharField(max_length=100)
    country = models.IntegerField()
    state = models.IntegerField() 
    phone = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.city}'
    



