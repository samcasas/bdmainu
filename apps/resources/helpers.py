import random
import string
import boto3
from django.conf import settings

class Helper:
    def responseRequest(self, status, msg, data, success):
        return {'success': success, 'message': msg,'data': data, 'status' : status }
    
    def generateTokenRandom(self, length):

        # Puedes elegir entre letras minúsculas, mayúsculas, dígitos, o combinaciones de ellos
        characters = string.ascii_letters + string.digits

        # Generar una cadena aleatoria
        random_string = ''.join(random.choice(characters) for i in range(length))

        return random_string
    
    def getS3Client(self):
        return boto3.client('s3',
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            region_name=settings.AWS_S3_REGION_NAME)