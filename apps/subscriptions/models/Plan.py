from django.db import models

class Plan(models.Model):
    ACTIVE = 1
    INACTIVE = 0

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    ]
    
    name = models.CharField(max_length=255)
    plan_openpay_id = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.name}'