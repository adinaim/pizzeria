from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator)

from apps.pizza.models import Pizza

User = get_user_model()

class Purchase(models.Model):

    ORDER_STATUS = (
        ('new', 'Новый'),
        ('processing','В процессе'),
        ('delivery', 'У курьера'),
        ('delivered','Доставлено')
            )
    CASHBACK_USAGE = (
        ('yes', 'Использовать баллы'),
        ('no', 'Не использовать баллы')
    )



    user = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='orders',
        blank=True,
        null=True
    )   # phone # comments     
    pizza = models.ManyToManyField(
        to=Pizza,
        through='Items',
    )
    address = models.CharField(max_length=80, blank=True)   # объединить все
    street = models.CharField(max_length=50)
    house = models.CharField(max_length=6)
    apt = models.CharField(max_length=4, blank=True)
    doorway = models.CharField(max_length=2, blank=True)
    code = models.CharField(max_length=6, blank=True)
    floor = models.CharField(max_length=2, blank=True)

    order_id = models.CharField(max_length=58, blank=True)
    total_sum = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # code = models.CharField(max_length=6, blank=True)

    cashback = models.CharField(max_length=22, choices=CASHBACK_USAGE, default='no')

    comment = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'Заказ № {self.order_id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_id:
            self.order_id = str(self.created_at)[9:16].replace(':', '-').replace(' ', '-')      # str(self.user.username) + '-' + 
        if not self.address:
            self.address = self.street + ', ' + self.house + ', ' + self.apt + ', ' + self.doorway + ', ' + self.code + ', ' + self.floor
        return self.order_id, self.address

    # def create_code(self):
    #     code = get_random_string(length=6, allowed_chars=self.RANDOM_STRING_CHARS)
    #     if Purchase.objects.filter(code=code).exists():
    #         self.create_code()
    #     self.code = code
    #     self.save()

    class Meta:
        verbose_name = 'Покупка пиццы'
        verbose_name_plural = 'Покупки пицц'


class Items(models.Model):

    PIZZA_SIZES=(
        ('l','Большая'),
        ('s','Маленькая')
        )

    order = models.ForeignKey(
        to=Purchase,
        on_delete=models.SET_NULL, 
        related_name='items',
        null=True
    )
    pizza = models.ForeignKey(
        to=Pizza,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(20)])
    size = models.CharField(max_length=256, default="s", choices=PIZZA_SIZES)

    def __str__(self):
        return f'Заказ № '

    class Meta:
        verbose_name = 'Объект корзины'
        verbose_name_plural = 'Объекты корзины'