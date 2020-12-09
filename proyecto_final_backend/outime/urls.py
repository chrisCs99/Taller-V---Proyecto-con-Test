from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from outime import views
from outime.api import user_viewset
from outime.api.compra_viewset import VentaViewSet, PagosViewSet
from outime.api.producto_viewset import ProductoViewSet
from outime.api.categoria_viewset import CategoriaViewSet
from outime.api.user_viewset import UserViewSet
from outime.views import *

router = routers.DefaultRouter()
router.register(r'producto', ProductoViewSet)
router.register(r'categoria', CategoriaViewSet)
router.register(r'usr_stat', UserViewSet)
router.register(r'venta', VentaViewSet)
router.register(r'pago', PagosViewSet)

urlpatterns = [
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/<int:pk>', views.CategoriaListView, name='categoria_detail'),
    path('categorias/crear/', CategoriaCreate.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/edit', CategoriaUpdate.as_view(), name='categoria_edit'),
    path('categorias/<int:id>/delete', views.CategoriaDelete, name='categoria_delete'),

    path('productos/', views.ProductoListView.as_view(), name='producto_list'),
    path('productos/<int:pk>', views.ProductoListView.as_view(), name='producto_detail'),
    path('productos/crear/', ProductoCreate.as_view(), name='producto_create'),
    path('productos/<int:pk>/edit', ProductoUpdate.as_view(), name='producto_edit'),
    path('productos/<int:id>/delete', views.ProductoDelete, name='producto_delete'),

    path('api/login_user/', user_viewset.login_usuario, name='login_usr'),

    path('ventas/', views.VentaListView.as_view(), name='venta_list'),
    path('ventas/detalle/<int:id>/', views.verCompra, name='venta_detail'),
    path('ventas/detalle/aprobarVenta/', views.pago_aceptado, name='venta_aprobada'),
    path('ventas/detalle/rechazarVenta/', views.pago_anulado, name='venta_rechazada'),
    path('ventas/detalle/anularVenta/', views.anular_venta, name='venta_anular'),
    path('ventas/detalle/entregaVenta/', views.producto_entregado, name='venta_entregada'),

    path('usuarios/', views.inicioUsuario, name='usuarios'),
    path('usuarios/create/', views.createUsuario, name='usuarios_create'),
    path('usuarios/editar/<int:id>/', views.editUsuario, name='usuarios_edit'),
    path('usuarios/delete/<int:id>/', views.delUsuario, name='usuarios_delete'),

    path('movstock/', views.MovimientoStockListView.as_view(), name='movstock_list'),

    url(r'^', include(router.urls)),
]
