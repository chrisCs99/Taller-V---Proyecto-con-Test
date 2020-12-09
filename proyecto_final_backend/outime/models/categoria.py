from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(null=False, max_length=2000)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "categoria"
