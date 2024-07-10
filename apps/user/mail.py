from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

class Mail:

    def __init__(self, context, content, template):
        self.context = context
        self.content = content
        self.template = template
    
        try:
            template = get_template(self.template)
            html_content = template.render(self.content)
            email = EmailMultiAlternatives(
                self.context['title'],
                self.context['description'],
                settings.EMAIL_HOST_USER,
                [self.context['to_email']],
            )

            email.attach_alternative(html_content, 'text/html')
            email.send()
        except KeyError as e:
            raise ValueError(f"Falta la clave necesaria en el contexto: {e}")
        except Exception as e:
            raise ImproperlyConfigured(f"Error al enviar el correo: {e}")
        
