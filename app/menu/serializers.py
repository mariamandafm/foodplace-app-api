from rest_framework import serializers

from core.models import FoodItem


class FoodItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'price', 'available']
        read_only_fields = ['id']


class FoodItemDetailSerializer(FoodItemSerializer):

    class Meta(FoodItemSerializer.Meta):
        fields = FoodItemSerializer.Meta.fields + ['description']
