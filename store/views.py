from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Collection, Product
from .serializers import ProductSerializer,CollectionSerializer
from django.db.models import Count
# Create your views here.

class ProductList(ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.select_related("collection").all()
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request':self.request}

# class ProductList(APIView):
#     def get(self,request):
#         query_set=Product.objects.select_related("collection").all()
#         serializer=ProductSerializer(query_set,many=True,context={'request':request})
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer=ProductSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
        

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def delete(self,request,pk):
         product= get_object_or_404(Product,pk=pk)
         if product.orderitems.count()> 0:
            return Response ({'error':'Product cannot be deleted because it is associated with order items'},
                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
         product.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)  
     
    
            
  
  

  
#   Working with collections

class CollectionList(ListCreateAPIView):
    queryset=Collection.objects.annotate(
            products_count=Count('products')
        )
    serializer_class=CollectionSerializer

@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    collection= get_object_or_404(Collection.objects.annotate(
        products_count=Count('products')),pk=pk)
    if request.method == "GET":
        serializer=CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer= CollectionSerializer(collection,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
    elif request.method == "DELETE":
        if collection.products_count>0:
            return Response({'error':'Collection cannot be deleted because it is associated with products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset=Collection.objects.all()
    serializer_class=CollectionSerializer
    
    def delete(self, request, pk):
        collection=get_object_or_404(Collection,pk=pk)
        if collection.products_count>0:
            return Response({'error':'Collection cannot be deleted because it is associated with products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    