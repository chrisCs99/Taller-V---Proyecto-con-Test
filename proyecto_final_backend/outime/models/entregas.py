from django.db import models

from outime.models.ventas import Venta


class Entregas(models.Model):
    direccion_entrega = models.CharField(null=False, max_length=5000)
    latitud = models.CharField(null=True, blank=True, max_length=1000)
    longitud = models.CharField(null=True, blank=True, max_length=10000)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='venta', default=0)

    class Meta:
        db_table = "entrega"
