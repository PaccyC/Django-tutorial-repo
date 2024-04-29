from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .filters import ProductFilter
from .models import Collection, OrderItem, ProductReview, Product, Cart,CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer
from store.pagination import DefaultPagination
from django.db.models import Count
# Create your views here.


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


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'last_updated']

    # MANUAL FILTERING

    # def get_queryset(self):
    #     queryset=Product.objects.all()
    #     collection_id=self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset=queryset.filter(collection_id=collection_id)

    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with order items'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


#   Working with collections


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')
    )
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs["pk"]).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it is associated with products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return ProductReview.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk'], }

    # Working with cart


class CartViewSet(CreateModelMixin,
                  DestroyModelMixin,
                  RetrieveModelMixin, 
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related("cartitems__product").all()
    serializer_class = CartSerializer



class CartItemViewSet(ModelViewSet):
    http_method_names =["get",'post','patch','delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
            return
        return CartItemSerializer
    def get_queryset(self):
        
        return CartItem.objects.\
              filter(cart_id=self.kwargs['cart_pk']) \
                .select_related('product')  
                
                
    def get_serializer_context(self):
        return {'cart_id':self.kwargs["cart_pk"]}      