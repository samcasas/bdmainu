from django.conf import settings
from django.templatetags.static import static
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


class Mail:

    def __init__(self):
        pass
    
    def send(self, context, content, template):
        
        template = get_template(template)
        content = template.render(content)
        email = EmailMultiAlternatives(
            context['title'],
            context['description'],
            settings.DEFAULT_FROM_EMAIL,
            [context['to_email']],
        )

        email.attach_alternative(content, 'text/html')
        email.send()
    
    def send_confirmation_mail(self, request, user_data):

        frontend_url = settings.FRONTEND_URL
        logo_url = request.build_absolute_uri(static('assets/images/logo.png'))
        coffe_url = request.build_absolute_uri(static('assets/images/coffe.png'))
        
        content = {
                    "name" : user_data['name'], 
                    "logo" : logo_url,
                    "coffe": coffe_url,
                    "url" : frontend_url + 'success-confirmation/' + user_data['token'],
                    "privacity": frontend_url + '',
                    "terms": frontend_url + '',
                }
            
        confirmation_context = {
                    'title': 'Confirma tu cuenta',
                    'description': 'Ya estas a un paso...',
                    'to_email': user_data['email'],
                }
            
        self.send(confirmation_context, content,'confirmation.html')
        
        
        
