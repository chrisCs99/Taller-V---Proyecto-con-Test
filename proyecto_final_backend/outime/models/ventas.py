from django.contrib.auth.models import User
from django.db import models
from django_fsm import FSMIntegerField, transition
from outime.repositories.extras import SimplificadorDetalle


class Venta(models.Model):
    fecha_hora = models.DateTimeField(null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario', default=0)
    total_vendido = models.DecimalField(null=False, default=0, decimal_places=4, max_digits=9999)
    nit = models.CharField(null=True, max_length=2000)
    nombre_factura = models.CharField(null=True, max_length=2000)
    ESTADO_CREADO = 0
    ESTADO_PAGADO = 1
    ESTADO_PAGADO_ACEPTADO = 2
    ESTADO_PAGADO_RECHAZADO = -1
    ESTADO_ENTREGADO = 3
    ESTADO_ANULADO = -2
    ESTADO_INICIADO = -5

    ESTADOS = (
        (ESTADO_CREADO, 'Creado'),
        (ESTADO_PAGADO, 'Pagado'),
        (ESTADO_PAGADO_ACEPTADO, 'Pago Aceptado'),
        (ESTADO_PAGADO_RECHAZADO, 'Pago Rechazado'),
        (ESTADO_ENTREGADO, 'Entregado'),
        (ESTADO_ANULADO, 'Anulado'),
        (ESTADO_INICIADO, 'Iniciado'),
    )
    estado = FSMIntegerField(choices=ESTADOS, default=ESTADO_INICIADO, protected=True)

    @transition(estado, source=ESTADO_INICIADO, target=ESTADO_CREADO)
    def crearCompra(self, lista_productos):
        for producto in lista_productos:
            # f = producto.split(',')
            SimplificadorDetalle.crearDetalle(producto, self.id)

    @transition(estado, source=ESTADO_CREADO, target=ESTADO_PAGADO)
    def pagar(self):
        pass

    @transition(estado, source=ESTADO_PAGADO, target=ESTADO_PAGADO_ACEPTADO)
    def pagoAceptado(self):
        pass

    @transition(estado, source=ESTADO_PAGADO_ACEPTADO, target=ESTADO_ENTREGADO)
    def pagoEntregado(self):
        pass

    @transition(estado, source=ESTADO_PAGADO, target=ESTADO_PAGADO_RECHAZADO)
    def pagoRechazado(self):
        pass

    @transition(estado, source=[ESTADO_CREADO, ESTADO_PAGADO, ESTADO_PAGADO_ACEPTADO], target=ESTADO_ANULADO)
    def ventaAnulada2(self, idventa):
        SimplificadorDetalle.ventaAnulada(idventa)

    def __str__(self):
        return self.id + ' - ' + self.nombre_factura

    class Meta:
        db_table = "venta"