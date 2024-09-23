from django.db import models
from datetime import datetime
from apps.subscriptions.models.PromotionalCode import PromotionalCode
from apps.subscriptions.models.Plan import Plan

class Subscription(models.Model):
    user_id = models.IntegerField()
    plan_id = models.IntegerField()
    code_id = models.IntegerField(null=True)
    paymentMethod_id = models.IntegerField(null=True)
    expiration_date= models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.plan_id} {self.expired}'
    

    # BUSSINES RULES
    @classmethod
    def code_validation(cls, code, plan_id):
        try:
            codeObj =  PromotionalCode.getObjectCode(code)

            if codeObj.plan_id != plan_id :
                return {"isValid": False, "message": "El código ingresado no coincide con el plan seleccionado."}
            
            if codeObj.amount == 0 :
                return {"isValid": False, "message": "El código ingresado no es válido."}
            
            current_date = datetime.now().date()  # Obtiene la fecha actual
            if codeObj.end_date < current_date: 
                return {"isValid": False, "message": "El código ha expirado."}
            
            return {"isValid": True, "message": "Código aplicado correctamente."} 
        
        except PromotionalCode.DoesNotExist:
            return {"isValid": False, "message": "El código ingresado no es válido."}