from rest_framework import routers
from .views import UsuarioViewSet
from django.contrib import admin
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'users', UsuarioViewSet)

urlpatterns = router.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),  # <--- API base
]
