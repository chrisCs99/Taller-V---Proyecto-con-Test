from django import forms

from outime.models.ventas import Venta


class FormVenta(forms.Form):
    usuario = forms.IntegerField()
    fecha_hora = forms.DateTimeField()
    total = forms.DecimalField()
    nombre_factura = forms.CharField(initial='NA')
    nit = forms.CharField(initial='NA')
    razon = forms.CharField()
    class Meta:
        model = Venta
        fields = '__all__'