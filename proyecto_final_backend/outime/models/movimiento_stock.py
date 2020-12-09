from django.db import models
from django_fsm import FSMIntegerField, transition

from outime.models.producto import Producto
from outime.models.ventas import Venta


class Movimiento_Stock(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='producto_movimiento', default=0)
    id_referencia = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='referencia', default=0)
    cantidad = models.IntegerField(null=False, default=0)
    INGRESO = 0
    EGRESO = 1

    ESTADOS = (
        (INGRESO, 'Ingreso'),
        (EGRESO, 'Egreso'),
    )
    tipo_movimiento = FSMIntegerField(choices=ESTADOS, default=EGRESO, protected=True)

    @transition(tipo_movimiento, source=EGRESO, target=INGRESO)
    def incrementarValor(self):
        pass

    class Meta:
        db_table = "moviento_stock"
