from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    PizzaViewSet,
    ConcretePizzaViewSet
    )


router = DefaultRouter()
router.register('pizza', PizzaViewSet)
router.register('concrete-pizza', ConcretePizzaViewSet)





urlpatterns = [

]

urlpatterns += router.urls