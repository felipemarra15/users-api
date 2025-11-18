from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def healthz(_request):
    # Healthcheck simple que NO toca la DB
    return JsonResponse({"status": "ok"}, status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),
    path('healthz', healthz),   # <- healthcheck para probes
]
