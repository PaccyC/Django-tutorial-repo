from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.db.models import Count
from django.utils.html import format_html
from . import models
# Register your models here.


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["title","price","inventory_status","collection__title"]
    list_editable=['price']
    list_per_page=10
    list_select_related= ["collection"]
    
    def collection__title(self,product):
        return product.collection.title
    
    @admin.display(ordering="inventory")
    def inventory_status(self,product):
        if product.inventory < 10:
            return "LOW"
        return 'OK'


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=["title","products__count"]
    
    @admin.display(ordering="products__count")
    def products__count(self,collection):
        return format_html('<a href="https://google.com">{}</a>',collection.products__count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products__count= Count('product')
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=["first_name","last_name","membership_status"]
    list_editable=['membership_status']
    list_per_page=10
    
    
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=["id","placed_at","customer"]    
    