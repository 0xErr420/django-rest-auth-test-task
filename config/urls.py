from django.urls import include, path
from django.contrib import admin
from api.authentication.urls import auth_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('api/auth/', include(auth_urls)),
]
