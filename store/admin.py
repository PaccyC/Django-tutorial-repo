from typing import Any
from django.contrib import admin ,messages
from django.db.models.query import QuerySet
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html,urlencode
from . import models

# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title="inventory"
    parameter_name="invetory"
    def lookups(self, request, model_admin):
        return [
            ("<10","LOW")
        ]
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
         if self.value == '<10':
             return queryset.filter(inventory__lt=10)




@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields=["collection"]
    prepopulated_fields ={
        'slug':['title']
    }
    actions= ["clear_inventory"]
    list_display=["title","price","inventory_status","collection__title"]
    list_editable=['price']
    list_per_page=10
    list_filter= ["collection","last_updated",InventoryFilter]
    list_select_related= ["collection"]
    search_fields=["title"]
    def collection__title(self,product):
        return product.collection.title
    
    @admin.display(ordering="inventory")
    def inventory_status(self,product):
        if product.inventory < 10:
            return "LOW"
        return 'OK'
    
    
    @admin.action(description="Clear inventory")
    def clear_inventory(self,request,queryset):
        
        updated_count=queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products have been successfully updated",
            messages.SUCCESS
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=["title","products__count"]
    search_fields=["title"]
    
    @admin.display(ordering="products__count")
    def products__count(self,collection):
        url=(reverse("admin:store_product_changelist")
             + '?'
             + urlencode({'collection__id':str(collection.id)})
             )
        return format_html('<a href="{}">{}</a>',url,collection.products__count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products__count= Count('product')
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=["first_name","last_name","membership_status"]
    list_editable=['membership_status']
    list_per_page=10
    search_fields=["first_name__istartswith","last_name__istartswith"]
    
 

class OrderItemInline(admin.TabularInline):
    autocomplete_fields=["product"]
    model=models.OrderItem   
    
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields:["customer"]
    inlines=[OrderItemInline]
    list_display=["id","placed_at","customer"]    
    