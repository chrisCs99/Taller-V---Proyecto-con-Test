from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from outime.models.categoria import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Categoria
		fields = '__all__'


class CategoriaViewSet(viewsets.ModelViewSet):
	queryset = Categoria.objects.all()
	serializer_class = CategoriaSerializer

