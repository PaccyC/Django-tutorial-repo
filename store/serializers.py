from rest_framework import serializers
from decimal import Decimal
from store.models import Cart, CartItem, Product,Collection,ProductReview


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
    
    

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id","title","price"]    
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductReview
        fields=['id','name','description','date']
        
        
        
    def create(self, validated_data):
        product_id=self.context['product_id']
        
        return ProductReview.objects.create(product_id=product_id,**validated_data)
    
    
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem   
        fields=["id","quantity","product","total_price"] 
        
    product=SimpleProductSerializer()    
    total_price=serializers.SerializerMethodField('get_total_price')
    
    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity *  cart_item.product.price

class CartSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    cartitems=CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField("get_total_price")
    
    class Meta:
        model=Cart    
        fields=["id","cartitems","total_price"]
        
    def get_total_price(self,cart:Cart):
        return   sum([item.quantity * item.product.price  for item in cart.cartitems.all()]) 
    
    
    
