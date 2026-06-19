from rest_framework import serializers, viewsets
from .models import Proyecto

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ['id', 'titulo', 'categoria']

class ProyectoViewSet(viewsets.ModelViewSet):  
    queryset = Proyecto.objects.all().order_by('-creado_en')
    serializer_class = ProyectoSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']  