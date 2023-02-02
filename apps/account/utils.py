import re
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def normalize_phone(phone):
    phone = re.sub('[^0-9]', '', phone)
    if phone.startswith('0'):
        phone = f'996{phone[1:]}'
    if not phone.startswith('996'):
        phone = f'996{phone}'
    phone = f'+{phone}'
    return phone

def send_activation_code(instance):
    html_message = render_to_string(
            'account/code_mail.html',
            {'activation_code': instance.activation_code}
            )
    send_mail(
            'Подтверждение адреса электронной почты',
            '',
            settings.EMAIL_HOST_USER,
            [instance.email],
            html_message=html_message,
            fail_silently=False   
            )