from rest_framework import serializers

from store.models import Product, ShoppingCartItem


class CartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, max_value=100)

    class Meta:
        model = ShoppingCartItem
        fields = ('product', 'quantity')


class ProductSerializer(serializers.ModelSerializer):
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)
    cart_items = serializers.SerializerMethodField()
    # price = serializers.FloatField(min_value=1.00, max_value=100000)
    price = serializers.DecimalField(min_value=1.00, max_value=100000,
                                     max_digits=None, decimal_places=2)
    sale_start = serializers.DateTimeField(
        required=False,
        input_formats=['%Y-%m-%d %I:%M %p'], format=None, allow_null=True,
        help_text="Accept format is '2020-01-01 12:01 AM'",
        style={'input_type': 'text', 'placeholder': '2020-01-01 12:01 AM'}
    )
    sale_end = serializers.DateTimeField(
        required=False,
        input_formats=['%Y-%m-%d %I:%M %p'], format=None, allow_null=True,
        help_text="Accept format is '2020-01-01 12:01 PM'",
        style={'input_type': 'text', 'placeholder': '2020-01-01 12:01 PM'}
    )
    photo = serializers.ImageField(default=None)
    warranty = serializers.FileField(write_only=True, default=None)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'sale_start', 'sale_end',
                  'is_on_sale', 'current_price', 'cart_items', 'photo', 'warranty')

    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data

    def update(self, instance, validated_data):
        if validated_data.get('warranty', None):
            instance.description += '\n\n Warranty Information:\n'
            instance.descriptoin += b';'.join(validated_data['warranty'].readlines()).decode()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        validated_data.pop('warranty')
        return Product.objects.create(**validated_data)


class ProductStatSerializer(serializers.Serializer):
    stats = serializers.DictField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
        )
    )




