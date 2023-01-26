# from django.core.mail import send_mail
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
#
# from .models import CustomUser, UserProfile
#
#
# @receiver(post_save, sender=CustomUser)
# def create_profile(sender, instance, created, **kwargs):
#     """Сигнал Для создания Пользователя и его Профиль"""
#     if created:
#         # Отправляем электронное письмо со ссылкой для подтверждения адреса электронной почты
#         send_mail(
#             "Подтверждение адреса электронной почты",
#             f"http://127.0.0.1:8000/users/email/verification/{instance.email_verify}",
#             settings.EMAIL_HOST_USER,
#             [f"{instance.email}"],
#             fail_silently=False
#         )
#
#         # Создаем профиль пользователя
#         UserProfile.objects.create(user=instance)
