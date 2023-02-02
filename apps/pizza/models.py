from django.db import models



class Pizza(models.Model):

    SIZE_CHOISES = (
            ('30', 30),
            ('40', 40)
        )

# (
# 30, (‘weight’: ‘360 грамм’, ‘price’: 420),
# 40, (‘weight’: ‘560 грамм’, ‘price’: 620)
# )

    image = models.CharField(max_length=200, verbose_name='image')
    title = models.CharField(max_length=10, unique=True, primary_key=True)
    desc = models.CharField(max_length=200)
    # size = models.CharField(max_length=100, choices=SIZE_CHOISES)
    # weight = models.CharField(max_length=50, blank=True)
    # price = models.CharField(max_length=50, blank=True)
    size = models.JSONField(blank=True, default=list)

    def __str__(self) -> str:
        return self.title




    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'
    
