from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Pizza, ConcretePizza

User = get_user_model()


class PizzaCreateSerialiazers(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ' __all__'

    def create(self, validated_data):
        pizza = Pizza.objects.create(**validated_data)
        return pizza


class PizzaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ' __all__'


class PizzaListSeriaizers(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = '__all__'


# class ConcretePizzaCreateSerialiazers(serializers.ModelSerializer):
#     class Meta:
#         model = ConcretePizza
#         fields = ' __all__'

#     def create(self, validated_data):
#         pizza = ConcretePizza.objects.create(**validated_data)
#         return pizza


# class ConcretePizzaSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ConcretePizza
#         fields = ' __all__'


# class ConcretePizzaListSeriaizers(serializers.ModelSerializer):
#     class Meta:
#         model = Pizza
#         fields = '__all__'

# class PizzaRetrieveSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Pizza
#         fields = ['title', 'image']

#     def to_representation(self, instance: Pizza):
#         pizza = instance.pizza.all()
#         representation = super().to_representation(instance)  
#         representation['pizza'] = ConcretePizzaSerializers(instance=pizza).data