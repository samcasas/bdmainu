from django.db import models

class Benefit(models.Model):
    ACTIVE = 1
    INACTIVE = 0

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    ]
    
    plan_id = models.IntegerField(null=True)
    benefit = models.TextField(max_length=50)
    order = models.IntegerField(null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.benefit}'