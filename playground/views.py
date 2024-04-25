from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Sum,Max,Min
from django.db.models import Q,F,Count
from store.models import Customer, Product,Order
# Create your views here.

    
def say_hello(request):
    
    # query_set=Product.objects.filter(inventory=F('collection__id'))
    # query_set= Product.objects.prefetch_related("promotions").select_related('collection').all()
    query_set=Order.objects.select_related('customer').prefetch_related('orderitem_set').order_by("-placed_at")[:5]
    
    # Aggregating objects
    result= Customer.objects.annotate(order_count=Count("order"))
    
    
    return render(request,'hello.html',{'name':'Noel','orders':list(query_set),'result':result},)