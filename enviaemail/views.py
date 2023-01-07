from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_email(first_name, last_name, email):
    html_content = render_to_string("welcome_template.html", {"nome": first_name, "sobrenome": last_name})
    text_content = strip_tags(html_content) 

    email_sent = EmailMultiAlternatives("Seja bem vindo", text_content, settings.EMAIL_HOST_USER, [email])
    email_sent.attach_alternative(html_content, "text/html")
    email_sent.send()

