from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import CreateView, UpdateView

from outime.models.movimiento_stock import Movimiento_Stock

@method_decorator(staff_member_required, name='dispatch')
class MovimientoStockListView(generic.ListView):
    model = Movimiento_Stock

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovimientoStockListView, self).get_context_data(**kwargs)
        return context