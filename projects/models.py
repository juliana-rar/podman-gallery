from django.db import models
from rest_framework.permissions import AllowAny

class Proyecto(models.Model):
    titulo = models.CharField(max_length=200)
    titulo_en = models.CharField("Title (EN)", max_length=200, blank=True)
    categoria = models.CharField(max_length=3000)
    categoria_en = models.CharField("Category (EN)", max_length=3000, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        app_label = 'projects'

class IdeaPrivada(models.Model):
    permission_classes = [AllowAny]
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)  

    class Meta:
        verbose_name_plural = "Ideas privadas"
        ordering = ['-creado_en']

    def __str__(self):
        return self.titulo