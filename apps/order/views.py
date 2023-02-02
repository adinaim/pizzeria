from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny

from .models import Purchase
from .serializers import (
    PurchaseSerializer,
    PurchaseHistorySerializer,
    PurchaseListSerializer,
    PurchaseRetrieveSerializer
)


class OrderViewSet(mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]   

    def get_queryset(self):
        user = self.request.user
        email = user.email
        return Purchase.objects.filter(user=email)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class OrderViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return PurchaseListSerializer
        elif self.action == 'retrieve':
            return PurchaseRetrieveSerializer
        return PurchaseSerializer


class OrderHistoryView(ListAPIView):
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        email = user.email
        return Purchase.objects.filter(user=email)