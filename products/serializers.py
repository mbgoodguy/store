from rest_framework import fields
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from products.models import Basket, Product, ProductCategory


class ProductSerializer(ModelSerializer):
    category = SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'quantity', 'image', 'id', 'category')


class BasketSerializer(ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'sum', 'total_sum', 'total_quantity', 'created_timestamp',)
        read_only_fields = ('created_timestamp',)

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()
