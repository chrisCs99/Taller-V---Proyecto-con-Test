from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import CreateView, UpdateView

from outime.models.categoria import Categoria

@method_decorator(staff_member_required, name='dispatch')
class CategoriaListView(generic.ListView):
    model = Categoria

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriaListView, self).get_context_data(**kwargs)
        return context

@method_decorator(staff_member_required, name='dispatch')
class CategoriaDetailView(generic.DetailView):
    model = Categoria

@method_decorator(staff_member_required, name='dispatch')
class CategoriaCreate(CreateView):
    model = Categoria
    fields = '__all__'
    success_url = reverse_lazy('categoria_list')

@method_decorator(staff_member_required, name='dispatch')
class CategoriaUpdate(UpdateView):
    model = Categoria
    fields = '__all__'
    success_url = reverse_lazy('categoria_list')

@method_decorator(staff_member_required, name='dispatch')
def CategoriaDelete(request, id):
    Categoria.objects.filter(id=id).delete()
    return redirect('categoria_list')
