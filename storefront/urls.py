

from django.contrib import admin
from django.urls import path,include

admin.site.site_header = 'STOREFRONT ADMIN'
admin.site.index_title= "ADMIN"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("__debug__/", include("debug_toolbar.urls")),
    path("store/",include("store.urls")),
    path("playground/",include('playground.urls'))
]
