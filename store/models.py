from django.db import models
from django.core.validators import MinValueValidator,FileExtensionValidator
from uuid import uuid4
from django.conf import settings
from django.contrib import admin
from .validators import validate_file_size
# Create your models here.


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount=models.FloatField();    

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+')
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering=['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug =models.SlugField()
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,   
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT,related_name="products")
    promotions=models.ManyToManyField(Promotion,blank=True)
    
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering=['title']
        



class ProductImage(models.Model):
      product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
      image=models.ImageField(
          upload_to='store/images',
          validators=[validate_file_size])      


class Customer(models.Model):
   MEMBERSHIP_BRONZE = 'B'
   MEMBERSHIP_SILVER = 'S'
   MEMBERSHIP_GOLD = 'G'

   MEMBERSHIP_CHOICES = [
    (MEMBERSHIP_BRONZE, "Bronze"),
    (MEMBERSHIP_SILVER, "Silver"),
    (MEMBERSHIP_GOLD, 'Gold'),
   ]

   phone = models.CharField(max_length=255)
   birth_date = models.DateTimeField(null=True)
   membership_status = models.CharField(
        max_length=255, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
   user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
   
   def __str__(self) -> str:
       return f'{self.user.first_name} {self.user.last_name}'
   
   @admin.display(ordering="user__first_name")
   def first_name(self):
       return self.user.first_name
   
   @admin.display(ordering="user__last_name")
   def last_name(self):
       return self.user.last_name
   
   class Meta:
        ordering=['user__first_name','user__last_name']
        permissions=[
            ('view_history','Can View History')
        ]


class Order(models.Model):
   PAYMENT_PENDING= "P"
   PAYMENT_COMPLETE= "C"
   PAYMENT_FAILED= "F"

   PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, "PENDING"),
        (PAYMENT_COMPLETE, "COMPLETE"),
        (PAYMENT_FAILED, "FAILED"),
   ]

   placed_at=models.DateTimeField(auto_now_add=True)    
   payment_status= models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_PENDING)
   customer=models.ForeignKey(Customer,on_delete=models.PROTECT)
   
   class Meta:
       permissions=[
           ('cancel_order','Can Cancel Order')
       ]
   
   

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name="orderitems")
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)


class Address(models.Model):
    city= models.CharField(max_length=255)
    street= models.CharField(max_length=255)
    custome= models.ForeignKey(Customer,on_delete=models.CASCADE)   
    

class Cart(models.Model):
    # id=models.UUIDField(primary_key=True,default=uuid4)
    created_at=models.DateTimeField(auto_now_add=True) 

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cartitems')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])       
    
    
    

class Review(models.Model):
        product=models.ForeignKey(Product,on_delete=models.CASCADE)
        name=models.CharField(max_length=255)
        description=models.TextField()
        date_created=models.DateField(auto_now_add=True)



class ProductReview(models.Model):
        product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
        name=models.CharField(max_length=255)
        description=models.TextField()
        date=models.DateField(auto_now_add=True)
        