from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Pizza

User = get_user_model()


class PizzaCreateSerialiazers(serializers.ModelSerializer):

    

    # weight = serializers.CharField(max_length=50, blank=True)
    # price = serializers.CharField(max_length=50, blank=True)


    class Meta:
        model = Pizza
        fields = '__all__'


    def create(self, validated_data):

        # if validated_data['size'] == 30:
        #     weight = validated_data.get('weight')
        #     price = validated_data.get('price')
        #     pizza = Pizza.objects.get(weight=weight, price=price)

        #     weight = '360гр.'
        #     price = '420'
        #     pizza.save()
        # else:
        #     weight = validated_data.get('weight')
        #     price = validated_data.get('price')
        #     pizza = Pizza.objects.get(weight=weight, price=price)
        #     weight = '560гр.'
        #     price = '620'
        #     pizza.save()

        pizza = Pizza.objects.create(**validated_data)
        return pizza

    # def s(self):
    #     if self.validated_data['size'] == 30:
    #         weight = self.validated_data.get('weight')
    #         price = self.validated_data.get('price')
    #         pizza = Pizza.objects.get(weight=weight, price=price)
    #         weight = '360гр.'
    #         price = 420
    #         pizza.save()
    #     else:
    #         weight = self.validated_data.get('weight')
    #         price = self.validated_data.get('price')
    #         pizza = Pizza.objects.get(weight=weight, price=price)
    #         weight = '560гр.'
    #         price = 620
    #         pizza.save()
    #     return pizza


class PizzaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = '__all__'

    


class PizzaListSeriaizers(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['title', 'desc'] # size


class PizzaRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = '__all__'