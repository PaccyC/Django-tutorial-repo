from rest_framework import serializers
from decimal import Decimal
from store.models import Product,Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=["id","title","products_count"]
    # id=serializers.IntegerField()
    # title=serializers.CharField(max_length=255)
    products_count=serializers.IntegerField(read_only=True)
    
    
    
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id","title","description","slug","inventory","price","price_with_tax","collection"]
    # id=serializers.IntegerField()
    # title=serializers.CharField(max_length=255)
    # unit_price=serializers.DecimalField(max_digits=6,decimal_places=2,source="price")
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    # collection=serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )
    
    def  calculate_tax(self,product:Product):
        return product.price * Decimal(1.1)