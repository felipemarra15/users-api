from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
import os
import requests  # HTTP al microservicio

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()

        # URL del microservicio de notificaciones (env var o default para K8s)
        notify_url = os.getenv(
            "NOTIFY_URL",
            "http://notification-service.default.svc.cluster.local:8080/notify"
        )

        # Payload normalizado: 'telefono' siempre como string (o None)
        telefono_value = getattr(usuario, "telefono", None)
        payload = {
            "nombre": usuario.nombre,
            "mail": usuario.mail,  # clave esperada por el notification-service
            "telefono": (None if telefono_value is None else str(telefono_value))
        }

        # Llamada desacoplada: si falla la notificación, el alta igual queda en 201
        try:
            print("[notify] envío:", payload)  # debug
            r = requests.post(notify_url, json=payload, timeout=5)
            print("[notify] resp:", r.status_code, r.text[:500])  # debug
            r.raise_for_status()
        except Exception as e:
            # No rompemos el alta si falla la notificación
            print(f"[notify] error llamando a {notify_url}: {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
