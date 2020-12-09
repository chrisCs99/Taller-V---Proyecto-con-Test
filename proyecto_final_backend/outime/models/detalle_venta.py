from django.db import models

from outime.models.producto import Producto
from outime.models.ventas import Venta


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name="venta_detalle", on_delete=models.CASCADE, default=0)
    producto = models.ForeignKey(Producto, related_name="producto_detalle", on_delete=models.CASCADE, default=0)
    cantidad_vendida = models.IntegerField(default=0, null=False)
    precio_venta = models.DecimalField(null=False, default=0, decimal_places=4, max_digits=9999)

    class Meta:
        db_table = "detalleventa"