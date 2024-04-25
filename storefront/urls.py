

from django.contrib import admin
from django.urls import path,include

admin.site.site_header = 'STOREFRONT ADMIN'
admin.site.index_title= "ADMIN"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("playground/",include('playground.urls'))
]
