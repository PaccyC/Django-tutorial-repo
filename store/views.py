from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Collection, Product
from .serializers import ProductSerializer,CollectionSerializer
# Create your views here.

@api_view(["GET"])
def product_list(request):
    query_set=Product.objects.select_related("collection").all()
    serializer=ProductSerializer(query_set,many=True,context={'request':request})
    return Response(serializer.data)

@api_view(["GET"])
def product_detail(request,id):
    
      product= get_object_or_404(Product,pk=id)
      serilizer=ProductSerializer(product)
      return Response(serilizer.data)
  
  
@api_view(["GET"])
def collection_detail(request,pk):
      collection=get_object_or_404(Collection,pk=pk)
      serializer=CollectionSerializer(collection)
      return Response(serializer.data)