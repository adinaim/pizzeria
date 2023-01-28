from django.db import models



class Pizza(models.Model):

    image = models.ImageField(verbose_name='image')
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'
    

class ConcretePizza(models.Model):

    pizza = models.ForeignKey(
        to=Pizza,
        on_delete=models.CASCADE,
        related_name='pizza'
    )
    weight = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    price = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Конкретная Пицца'
        verbose_name_plural = 'Конкретные Пиццы'