from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    PizzaViewSet,
    )


router = DefaultRouter()
router.register('pizza', PizzaViewSet)





urlpatterns = [

]

urlpatterns += router.urls