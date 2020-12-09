from django.db import models

from outime.models.categoria import Categoria


class Producto(models.Model):
    nombre = models.CharField(null=False, max_length=2000)
    descripcion = models.CharField(null=False, max_length=2000)
    sku = models.CharField(null=False, max_length=2000)
    categoria = models.ManyToManyField(Categoria, related_name='categorias')
    precio = models.DecimalField(null=False, default=0, decimal_places=4, max_digits=9999)
    imagen_producto = models.ImageField(upload_to='image', null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "producto"