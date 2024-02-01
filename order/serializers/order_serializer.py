from rest_framework import serializers

from order.models import Order
from product.models import Product
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False, many=True)
    products_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, many=True
    )
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total

    class Meta:
        model = Product
        fields = ["product", "total", "products_id"]

    def create(self, validated_data):
        product_data = validated_data.pop("products_id")
        user_data = validated_data.pop("user")

        order = Order.objects.create(user_data=user_data)
        for products in product_data:
            order.product.add(products)

        return order
