from rest_framework import serializers

from .models import (
    Purchase, 
    Items
)
from apps.account.models import UserProfile
from .utils import cashback


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['pizza', 'quantity', 'size']


class PurchaseSerializer(serializers.ModelSerializer):
    items = ItemsSerializer(many=True) 

    class Meta:
        model = Purchase
        fields = ['order_id', 'created_at', 'updated_at', 'total_sum', 'address', 'items']

    def create(self, validated_data, *args, **kwargs):
        user = self.context['request'].user
        email = user.email
        profile = UserProfile.objects.get(user=email)
        p_cashback = profile.cashback

        items = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        order = super().create(validated_data) # Order.objects.create
        total_sum = 0
        orders_items = []
        for item in items:
            pizzas = (Items(
                order=order,
                pizza=item['pizza'],
                quantity=item['quantity'],
                size=item['size']
            ))
            orders_items.append(pizzas)

            if item['size'] == 's':
                price = item['pizza'].size.get('30').get('price')
            elif item['size'] == 'l':
                price = item['pizza'].size.get('40').get('price')

            total_sum += price * item['quantity']    # size   item['pizza'].price

            Items.objects.bulk_create(orders_items, *args, **kwargs)

            order.total_sum = total_sum

            if self.context['request'].user.is_authenticated and cashback=='yes' and self.p_cashback:
                cashback(self.context, order, total_sum)

            item['pizza'].save()
            order.save()

        return order


class PurchaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['order_id', 'pizza', 'status', 'created_at']


class PurchaseRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


class PurchaseHistorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Purchase
        fields = ('order_id', 'total_sum', 'status', 'created_at', 'pizza')