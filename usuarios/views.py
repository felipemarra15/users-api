from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
import os
import requests
import logging

logger = logging.getLogger(__name__)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()

        # ---- Enviar evento al microservicio de notificaciones ----
        notify_url = os.getenv("NOTIFY_URL", "http://notification-service:5000/notify")
        payload = {"nombre": usuario.nombre, "email": usuario.mail}

        try:
            resp = requests.post(notify_url, json=payload, timeout=3)
            resp.raise_for_status()
        except Exception as e:
            # No rompemos el alta si falla la notificación
            logger.warning("Fallo al notificar alta de usuario %s: %s", usuario.mail, e)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
