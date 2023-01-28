from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .serializers import (
    PizzaCreateSerialiazers,
    # ConcretePizzaCreateSerialiazers,
    PizzaListSeriaizers,
    # ConcretePizzaListSeriaizers,
    PizzaSerializers,
    # ConcretePizzaSerializers,
    # PizzaRetrieveSerializers
)


from .models import Pizza, ConcretePizza




class PizzaViewSet(ModelViewSet):
    queryset = Pizza.objects.all()
    permission_classes = IsAdminUser

    def get_serializer_class(self):
        if self.action == 'list':
            return PizzaListSeriaizers
        # elif self.action == 'retrieve':
        #     return PizzaRetrieveSerializers
        return PizzaSerializers

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions() 


# class ConcretePizzaViewSet(ModelViewSet):
#     queryset = ConcretePizza.objects.all()
#     permission_classes = IsAdminUser

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return ConcretePizzaListSeriaizers
#         return PizzaSerializers

#     def get_permissions(self):
#         if self.action in ['list', 'retrieve']:
#             self.permission_classes = [AllowAny]
#         if self.action in ['create', 'destroy', 'update', 'partial_update']:
#             self.permission_classes = [IsAdminUser]
#         return super().get_permissions() 