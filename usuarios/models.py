from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    mail = models.EmailField(unique=True)
    telefono = models.IntegerField()

    def __str__(self):
        return self.nombre

