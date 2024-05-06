from django.urls import path
from . import views
# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers


router=routers.SimpleRouter()
router.register("products",views.ProductViewSet,basename="products")
router.register("collections",views.CollectionViewSet)
router.register("carts",views.CartViewSet)
router.register("customers",views.CustomerViewSet)
router.register("orders",views.OrderViewSet)


# Child routers
products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')
products_router.register('images',views.ProductImageViewSet,basename='product-images')

carts_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
carts_router.register('items',views.CartItemViewSet,basename='cart-items')


# Images

urlpatterns=router.urls + products_router.urls + carts_router.urls