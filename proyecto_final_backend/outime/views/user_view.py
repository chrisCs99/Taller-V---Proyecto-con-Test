from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import CreateView, UpdateView

from outime.forms.user_form import UsersForm

@staff_member_required()
@transaction.atomic
def createUsuario(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            usuario = User()
            usuario.last_name = request.POST['last_name']
            usuario.first_name = request.POST['first_name']
            usuario.username = request.POST['username']
            usuario.email = request.POST['email']
            usuario.set_password(request.POST['password'])
            usuario.is_staff = True
            usuario.save()
            return redirect('/outime/usuarios/')
    else:
        usuarios = UsersForm()
        return render(request, 'outime/formuser.html', {'form': usuarios})

@staff_member_required()
@transaction.atomic
def editUsuario(request, id):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        form.fields['password'].required = False
        if form.is_valid():
            # try:
            usuario = User.objects.filter(id=id).first()
            usuario.last_name = request.POST['last_name']
            usuario.first_name = request.POST['first_name']
            usuario.email = request.POST['email']
            usuario.username = request.POST['username']
            usuario.groups.clear()
            if request.POST['password'] != '':
                usuario.set_password(request.POST['password'])
            usuario.save()
            return redirect('/outime/usuarios/')
            # except:
            #     render(request, 'usuarios/edituser.html', {'form': form})
        else:
            return HttpResponse(form.errors)
            # return redirect('/notas/usuarios/editar/' + str(id)+'/')
    else:
        if id is None:
            return HttpResponseForbidden()
        else:
            usuario = User.objects.filter(id=id).first()
            form = UsersForm(instance=usuario)
            form.fields['password'].required = False
            return render(request, 'outime/edituser.html', {'form': form, 'id': id})

@staff_member_required()
@transaction.atomic
def delUsuario(request, id):
    User.objects.filter(id=id).delete()
    return redirect('/outime/usuarios/')

@staff_member_required()
@transaction.atomic
def inicioUsuario(request):
    listaUserDoc = User.objects.filter(is_staff=True)
    listaUserEst = User.objects.filter(is_staff=False)
    usuarios = UsersForm()
    return render(request, 'outime/inicio.html', {'lstDoc': listaUserDoc, 'lstEst': listaUserEst})