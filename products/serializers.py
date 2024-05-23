from rest_framework import serializers, fields

from products.models import Inventory, Product, Category, Size, Cart


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'image', 'category')


class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    size = serializers.SlugRelatedField(slug_field='size', queryset=Size.objects.all())

    class Meta:
        model = Inventory
        fields = ('id', 'product', 'size', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    product = InventorySerializer()
    sum = fields.SerializerMethodField(required=False)

    def get_sum(self, obj):
        return Cart.get_product_sum(obj)

    class Meta:
        model = Cart
        fields = ('id', 'product', 'quantity', 'sum', 'created_timestamp')
        read_only_fields = ('created_timestamp', )
