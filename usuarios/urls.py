from django.urls import path
from .views import UsuarioViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = router.urls
