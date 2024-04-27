from django.urls import path
from . import views
# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers


router=routers.SimpleRouter()
router.register("products",views.ProductViewSet,basename="products")
router.register("collections",views.CollectionViewSet)


# Child router
products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

urlpatterns=router.urls + products_router.urls