from rest_framework import serializers

from core.models import (
    FoodItem,
    Order,
    )


class FoodItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'price', 'available', 'image', 'type']
        read_only_fields = ['id']


class FoodItemDetailSerializer(FoodItemSerializer):

    class Meta(FoodItemSerializer.Meta):
        fields = FoodItemSerializer.Meta.fields


class OrderSerializer(serializers.ModelSerializer):
    food_items = FoodItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'food_items', 'status', 'payment_method', 'total_price', 'total_items']
        read_only_fields = ['id']

    def create(self, validated_data):
        # query if the an order with status 'NOT_PLACED' exists for the user
        auth_user = self.context['request'].user
        order = Order.objects.filter(
            user=auth_user,
            status='NOT_PLACED'
        ).first()
        # if order exists, add food items to the order
        if order:
            food_items = validated_data.pop('food_items', [])
            for item in food_items:
                try:
                    item_obj = FoodItem.objects.get(
                        **item
                    )
                    order.food_items.add(item_obj)
                except FoodItem.DoesNotExist:
                    raise serializers.ValidationError(
                        'Food item does not exist.'
                    )
        else:
            # else create a new order
            food_items = validated_data.pop('food_items', [])
            auth_user = self.context['request'].user
            order = Order.objects.create(user=auth_user, **validated_data)
            for item in food_items:
                try:
                    item_obj = FoodItem.objects.get(
                        **item
                    )
                    order.food_items.add(item_obj)
                except FoodItem.DoesNotExist:
                    raise serializers.ValidationError(
                        'Food item does not exist.'
                    )

        return order
