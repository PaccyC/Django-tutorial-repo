from rest_framework import serializers
from decimal import Decimal
from store.models import Cart, CartItem, Customer, Order, OrderItem, Product,Collection,ProductReview


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
    
    product=SimpleProductSerializer()    
    total_price=serializers.SerializerMethodField('get_total_price')
    
    class Meta:
        model = CartItem   
        fields=["id","quantity","product","total_price"] 
        
    
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
    
    
    

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    
    # Validation
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Product with given id not found")
        return value
        
    # Preventing adding into cart same item, we only update it's quantity.We override save method
    # validated_date is a dictionary
    
    def save(self, **kwargs):
        cart_id= self.context.get('cart_id')
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']
        try:
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity +=quantity
            cart_item.save()
            
            self.instance=cart_item
        except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(cart_id=cart_id,**self.validated_data)
            
        return self.instance    
    class Meta:
        model=CartItem
        fields=["id","product_id","quantity"]
        
        

class UpdateCartItemSerializer(serializers.ModelSerializer):
    
    # Override update method
    def update(self, instance, validated_data):
        instance.quantity=validated_data.get('quantity',self.validated_data['quantity'])
        instance.save()
        return instance
    class Meta:
        model=CartItem
        fields=["quantity"]        
        
        
        # Customer profile serializer
        
        

class CustomerSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model=Customer     
        fields=["id","user_id","phone","birth_date","membership_status"]   
        
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    class Meta:
        model=OrderItem      
        fields=["id","product","quantity","unit_price"]  


class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    class Meta:
         model=Order        
         fields= ["id","customer","items","placed_at","payment_status"]