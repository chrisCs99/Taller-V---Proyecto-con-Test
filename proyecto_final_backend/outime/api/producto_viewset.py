from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from outime.models.producto import Producto


class ProductoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Producto
		fields = '__all__'


class ProductoViewSet(viewsets.ModelViewSet):
	queryset = Producto.objects.all()
	serializer_class = ProductoSerializer

	@action(methods=['POST'], detail=False)
	def get_lista_genero(self, request, *args, **kwargs):
		categoria = request.data['categoria']

		lista_juegos_genero = Producto.objects.filter(
			categoria=int(categoria)
		)
		result = ProductoSerializer(lista_juegos_genero, many=True)
		return Response(result.data, status=status.HTTP_200_OK)

	@action(methods=['POST'], detail=False)
	def get_juego_id(self, request, *args, **kwargs):
		productoId = request.data['id']

		producto = Producto.objects.filter(
			id=int(productoId)
		)
		result = ProductoSerializer(producto, many=True)
		return Response(result.data, status=status.HTTP_200_OK)