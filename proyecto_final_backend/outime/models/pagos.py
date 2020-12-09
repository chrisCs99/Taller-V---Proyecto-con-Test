from django.db import models
from django_fsm import FSMIntegerField, transition

from outime.models.ventas import Venta
from outime.repositories.extras import SimplificadorDetalle


class Pagos(models.Model):
    monto_pagado = models.ImageField(upload_to='comprante_pagos', null=True, blank=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='ventas_pago', default=0)
    ESTADO_PENDIENTE = 0
    ESTADO_PAGADO = 1
    ESTADO_APROBADO = 2
    ESTADO_ANULADO = -1

    ESTADOS = (
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_PAGADO, 'Pagado'),
        (ESTADO_APROBADO, 'Aprobado'),
        (ESTADO_ANULADO, 'Anulado'),
    )
    estado = FSMIntegerField(choices=ESTADOS, default=ESTADO_PENDIENTE, protected=True)

    @transition(estado, source=ESTADO_PENDIENTE, target=ESTADO_PAGADO)
    def subirPago(self, idventa):
        SimplificadorDetalle.cambioPendientePago(idventa)

    @transition(estado, source=ESTADO_PAGADO, target=ESTADO_APROBADO)
    def aprobarPago(self, idventa):
        SimplificadorDetalle.aprobadoPago(idventa)

    @transition(estado, source=[ESTADO_PAGADO, ESTADO_PENDIENTE], target=ESTADO_ANULADO)
    def anularPago(self, idventa):
        SimplificadorDetalle.pagoAnulado(idventa)

    @transition(estado, source=[ESTADO_PAGADO, ESTADO_PENDIENTE, ESTADO_APROBADO], target=ESTADO_ANULADO)
    def anularPago2(self):
        pass

    class Meta:
        db_table = "pagos"
