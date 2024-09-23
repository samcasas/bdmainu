from django.db import models


class PaymentMethod(models.Model):
    card = models.CharField(max_length=255)
    token_openpay_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.card}'
    