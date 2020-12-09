from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import CreateView, UpdateView

from outime.models.producto import Producto

@method_decorator(staff_member_required, name='dispatch')
class ProductoListView(generic.ListView):
    model = Producto

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductoListView, self).get_context_data(**kwargs)
        return context

@method_decorator(staff_member_required, name='dispatch')
class ProductoDetailView(generic.DetailView):
    model = Producto

@method_decorator(staff_member_required, name='dispatch')
class ProductoCreate(CreateView):
    model = Producto
    fields = '__all__'
    success_url = reverse_lazy('producto_list')

@method_decorator(staff_member_required, name='dispatch')
class ProductoUpdate(UpdateView):
    model = Producto
    fields = '__all__'
    success_url = reverse_lazy('producto_list')

@method_decorator(staff_member_required, name='dispatch')
def ProductoDelete(request, id):
    Producto.objects.filter(id=id).delete()
    return redirect('producto_list')
