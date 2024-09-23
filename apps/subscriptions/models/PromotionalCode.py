from django.db import models

class PromotionalCode(models.Model):

    ACTIVE = 1
    INACTIVE = 0

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    ]

    code = models.CharField(max_length=255)
    plan_id = models.IntegerField()
    amount = models.IntegerField() #CANTIDAD DE USOS PARA EL CODIGO
    months = models.IntegerField()
    end_date = models.DateField(null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code}'
    

    @classmethod
    def getObjectCode(cls, code):
        return cls.objects.get(code=code)
    
    @classmethod
    def discountCode(cls, code):
        try:
            promo_code = cls.getObjectCode(code)  # Busca el código promocional
            
            # Verificar si el código tiene usos restantes
            if promo_code.amount > 0:
                promo_code.amount -= 1  # Descuenta uno al campo `amount`
                promo_code.save()  # Guarda el cambio en la base de datos
                return {"success": True, "message": "Código aplicado correctamente.", "remaining_uses": promo_code.amount}
            else:
                return {"success": False, "message": "El código ya no tiene usos disponibles."}
        
        except cls.DoesNotExist:
            return {"success": False, "message": "El código no existe."}

        except Exception as e:
            return {"success": False, "message": f"Ocurrió un error inesperado: {str(e)}"}