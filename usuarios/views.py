from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
from django.core.mail import send_mail
from django.conf import settings

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()

        # --- Envío del correo ---
        try:
            asunto = "🎉 Bienvenido al sistema"
            mensaje = f"Hola {usuario.nombre}, tu registro fue exitoso.\n\nGracias por registrarte."
            destinatario = [usuario.mail]

            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                destinatario,
                fail_silently=False  # si hay error, lo mostramos abajo
            )

        except Exception as e:
            # ⚠️ no rompe el registro, pero lo loguea
            print(f"Error enviando correo a {usuario.mail}: {e}")
            return Response(
                {"detail": f"Usuario registrado, pero error al enviar correo: {str(e)}"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
