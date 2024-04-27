from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Collection, Product
from .serializers import ProductSerializer,CollectionSerializer
# Create your views here.

@api_view(["GET","POST"])
def product_list(request):
    if request.method == "GET":
        query_set=Product.objects.select_related("collection").all()
        serializer=ProductSerializer(query_set,many=True,context={'request':request})
        return Response(serializer.data)
    elif request.method == "POST":
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT"])
def product_detail(request,id):
    product= get_object_or_404(Product,pk=id)
    if request.method == "GET":
        serilizer=ProductSerializer(product)
        return Response(serilizer.data)
    elif request.method == "PUT":
        serilizer=ProductSerializer(product,data=request.data)
        if serilizer.is_valid(raise_exception=True):
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        
  
  
@api_view(["GET"])
def collection_detail(request,pk):
      collection=get_object_or_404(Collection,pk=pk)
      serializer=CollectionSerializer(collection)
      return Response(serializer.data)