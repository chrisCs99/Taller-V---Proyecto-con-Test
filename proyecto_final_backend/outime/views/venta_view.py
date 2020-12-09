import json
from argparse import Namespace
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import CreateView, UpdateView
from django.utils import timezone

from outime.forms.venta_form import FormVenta
from outime.models.detalle_venta import DetalleVenta
from outime.models.entregas import Entregas
from outime.models.pagos import Pagos
from outime.models.producto import Producto
from outime.models.ventas import Venta


@method_decorator(staff_member_required, name='dispatch')
class VentaListView(generic.ListView):
    model = Venta

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VentaListView, self).get_context_data(**kwargs)
        # context['prueba'] = "hola mundo"
        return context


@staff_member_required()
def verCompra(request, id):
    pago = Pagos.objects.filter(id_venta_id=id).first()
    detalleVenta = DetalleVenta.objects.filter(venta_id=id).all()
    entregas = Entregas.objects.filter(id_venta_id=id).first()
    return render(request, 'outime/venta_detail.html',
                  {'pago': pago, 'detalleventa': detalleVenta, 'entregas': entregas})


@staff_member_required()
@transaction.atomic
def pago_aceptado(request):
    pagoid = request.POST['id']
    pago = Pagos.objects.filter(id=pagoid).first()
    pago.aprobarPago(pago.id_venta.id)
    pago.save()
    return HttpResponse(status=200)


@staff_member_required()
@transaction.atomic
def producto_entregado(request):
    venta_id = request.POST['id']
    venta = Venta.objects.filter(id=venta_id).first()
    venta.pagoEntregado()
    venta.save()
    return HttpResponse(status=200)


@staff_member_required()
@transaction.atomic
def pago_anulado(request):
    pagoid = request.POST['id']
    pago = Pagos.objects.filter(id=pagoid).first()
    pago.anularPago(pago.id_venta.id)
    pago.save()
    return HttpResponse(status=200)


@staff_member_required()
@transaction.atomic
def anular_venta(request):
    venta_id = request.POST['id']
    venta = Venta.objects.filter(id=venta_id).first()
    venta.ventaAnulada2(venta.id)
    venta.save()
    return HttpResponse(status=200)
