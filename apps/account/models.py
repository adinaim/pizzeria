from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
# from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from .utils import send_activation_code

# User = get_user_model()

class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, phone, **extra_fields): # username, 
        if not email:
            raise ValueError("Вы не ввели Email")
        # if not username:
        #     raise ValueError("Вы не ввели Логин")
        if not phone:
            raise ValueError("Вы не ввели Телефон")
        if len(password) < 8:
            raise ValueError("Пароль должен содержать не менее 8 символов")
        user = self.model(
            email=self.normalize_email(email),
            # username=username,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, phone): # username
        return self._create_user(email, password, phone) # username

    def create_superuser(self, email, password, phone, **extra_fields): # username, phone
        # extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError(' is_superuser=True.')

        return self._create_user(
            email=email,
            # username=username,
            password=password,
            phone=phone,
            **extra_fields
        )


class CustomUser(AbstractBaseUser):
    """ Модель пользователя """
    RANDOM_STRING_CHARS = "1234567890"

    email = models.EmailField(max_length=100, unique=True, primary_key=True)
    phone = PhoneNumberField(null=True, region='KG', unique=True, blank=True)
    is_active = models.BooleanField(default=False)  # Статус активации
    is_staff = models.BooleanField(default=False)  # Статус админа
    activation_code = models.CharField(max_length=10, blank=True)
    # email_verify = models.UUIDField(default=uuid4())

    USERNAME_FIELD = 'email'  # Идентификатор для обращения
    REQUIRED_FIELDS = ['phone']  # Список имён полей для Superuser 'username', 

    objects = MyUserManager()

    def __str__(self):
        return f'{self.email}' #, self.email_verify}' # self.username

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = get_random_string(length=4, allowed_chars=self.RANDOM_STRING_CHARS)
        if CustomUser.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save()

    def email_verificate(self):
        self.is_active = True
        self.save(update_fields=['is_active'])


class UserProfile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE,
                                related_name='user') #settings.AUTH_USER_MODEL
    birthday = models.DateField(null=True)     # нужно ли
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = PhoneNumberField(null=True, region='KG', unique=True) #, required=True)
    cashback = models.CharField(max_length=7, blank=True, null=True)
    # address = models.CharField

    def __str__(self):
        return f'{self.user}'
# добавить адрес, чтобы каждый раз не заполнять


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """Сигнал Для создания Пользователя и его Профиль"""
    if created:
        # Отправляем электронное письмо со ссылкой для подтверждения адреса электронной почты
        send_activation_code(instance)

        # Создаем профиль пользователя
        UserProfile.objects.create(user=instance)




# def send_code(email, code):
#     html_message = render_to_string(
#         'booking/confirmation_mail.html',
#         {'confirmation_code': code}
#         )
        
#     send_mail(
#         'Подтверждение адреса электронной почты',
#         '',
#         settings.EMAIL_HOST_USER,
#         [instance.email],
#         html_message=html_message,
#         fail_silently=False   
#     )