from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

class Mail:

    def __init__(self, context, content, template):
        self.context = context
        self.content = content
        self.template = template
    
    def send(self):
        
        template = get_template(self.template)
        content = template.render(self.content)
        email = EmailMultiAlternatives(
            self.context['title'],
            self.context['description'],
            settings.EMAIL_HOST_USER,
            [self.context['to_email']],
        )

        email.attach_alternative(content, 'text/html')
        email.send()
        
