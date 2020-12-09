from decimal import Decimal

from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone, dateformat
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from outime.api.producto_viewset import ProductoSerializer
from outime.api.user_viewset import UserSerializer
from outime.models.detalle_venta import DetalleVenta
from outime.models.entregas import Entregas
from outime.models.pagos import Pagos
from outime.models.ventas import Venta


class VentaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Venta
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    venta = VentaSerializer(many=False, read_only=True)
    producto = ProductoSerializer(many=False, read_only=True)
    class Meta:
        model = DetalleVenta
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    id_venta = VentaSerializer(many=False, read_only=True)
    class Meta:
        model = Pagos
        fields = '__all__'

class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entregas
        fields = '__all__'


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    @action(methods=['POST'], detail=False)
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    @transaction.atomic
    def crear_venta(self, request, *args, **kwargs):
        lst_productos = request.data['producto']
        venta = Venta()
        venta.fecha_hora = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        venta.usuario = User.objects.filter(id=request.data['usrID']).first()
        venta.nombre_factura = request.data['nombre_factura']
        venta.nit = request.data['nit']
        venta.total_vendido = Decimal(request.data['precio_total'])
        venta.save()

        venta2 = Venta.objects.filter(id=venta.id).first()
        venta2.crearCompra(lst_productos)
        venta2.save()

        newEntrega = Entregas()
        newEntrega.direccion_entrega = request.data['direccionEntrega']
        newEntrega.latitud = request.data['latitud']
        newEntrega.longitud = request.data['longitud']
        newEntrega.id_venta = Venta.objects.filter(id=venta.id).first()
        newEntrega.save()

        newPago = Pagos()
        newPago.id_venta = Venta.objects.filter(id=venta.id).first()
        newPago.save()

        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def obtener_ventas_usuario(self, request, *args, **kwargs):
        list_venta = Venta.objects.filter(usuario_id=request.data['usrID']).all()
        result = VentaSerializer(list_venta, many=True, read_only=True)
        return Response(result.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def obtener_productos_venta(self, request, *args, **kwargs):
        list_venta = DetalleVenta.objects.filter(venta_id=request.data['ventaID']).all()
        result = DetalleVentaSerializer(list_venta, many=True, read_only=True)
        return Response(result.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def obtener_productos_venta_informacion(self, request, *args, **kwargs):
        list_venta = Pagos.objects.filter(id_venta_id=request.data['ventaID']).all()
        result = PagoSerializer(list_venta, many=True)
        return Response(result.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def obtener_productos_venta_informacion_entrega(self, request, *args, **kwargs):
        list_venta = Entregas.objects.filter(id_venta_id=request.data['ventaID']).all()
        result = EntregaSerializer(list_venta, many=True)
        return Response(result.data, status=status.HTTP_200_OK)

class PagosViewSet(viewsets.ModelViewSet):
    queryset = Pagos.objects.all()
    serializer_class = PagoSerializer

    @action(methods=['POST'], detail=False)
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    @transaction.atomic
    def comprobante_enviado_cambiar_valor(self, request, *args, **kwargs):
        pagoReal = Pagos.objects.filter(id_venta_id=request.data['ventaID']).first()
        pagoReal.monto_pagado = request.data['monto_pagado']
        pagoReal.subirPago(request.data['ventaID'])
        pagoReal.save()
        return Response(status=status.HTTP_200_OK)