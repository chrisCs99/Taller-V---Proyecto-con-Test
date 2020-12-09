from django.contrib.auth.models import User, Group
from django.test import TestCase

import request
import responses

# Create your tests here.
from django.utils import dateformat, timezone

from outime.api import user_viewset
from outime.models.categoria import Categoria
from outime.models.entregas import Entregas
from outime.models.movimiento_stock import Movimiento_Stock
from outime.models.pagos import Pagos
from outime.models.producto import Producto
from outime.models.ventas import Venta


class TestUser(TestCase):
    def setUp(self) -> None:
        usuario = User()
        usuario.last_name = 'Juan'
        usuario.first_name = 'Ramon'
        usuario.username = 'jramon'
        usuario.email = 'jramon@ex.com'
        usuario.set_password('test')
        usuario.save()
        grupo = Group.objects.filter(id=1).first()
        usuario.groups.add(grupo)

    def test_insert_user(self):
        usuario = User()
        usuario.last_name = 'Juan'
        usuario.first_name = 'Ramon'
        usuario.username = 'jramon5'
        usuario.email = 'jramon@ex.com'
        usuario.set_password('test')
        usuario.save()
        grupo = Group.objects.filter(id=1).first()
        usuario.groups.add(grupo)
        self.assertEquals(usuario.username, 'jramon5', 'No es igual al nombre')

class TestCategoria(TestCase):
    def crearCategoria(self):
        categoria = Categoria.objects.create(nombre='Test')
        self.assertIsNotNone(categoria, 'No existe ningun dato')

    def test_nombre_categoria(self):
        categoria = Categoria.objects.create(nombre='Test')
        self.assertEquals(categoria.nombre, 'Test', 'No es el mismo dato')
        categoria2 = Categoria.objects.create(nombre='Hola mundo')
        self.assertNotEquals(categoria2.nombre, 'Test2', 'Son iguales')

class TestProducto(TestCase):
    def test_CrearProducto(self):
        categoria1 = Categoria.objects.create(nombre='Probandos')
        categoria2 = Categoria.objects.create(nombre='FFFF')
        categoria1.save()
        categoria2.save()

        prod1 = Producto.objects.create(nombre='Pijamas', descripcion='Comoda y suave', precio=150,
                                        sku='530PA')

        prod2 = Producto.objects.filter(id=50).first()

        self.assertIsNotNone(categoria1, 'No existe ningun dato')
        self.assertIsNotNone(categoria2, 'No existe ningun dato')
        self.assertIsNotNone(prod1, 'No existe ningun dato')
        self.assertIsNone(prod2, 'El resultado es diferente de None')

class TestVenta(TestCase):
    def test_crearVenta(self):
        usr = User()
        usr.last_name = 'Juan'
        usr.first_name = 'Ramon'
        usr.username = 'jramon5'
        usr.email = 'jramon@ex.com'
        usr.set_password('test')
        usr.save()
        self.assertIsNotNone(usr, 'El usuario no existe')
        categoria1 = Categoria.objects.create(nombre='Probandos')
        categoria1.save()

        prod1 = Producto.objects.create(nombre='Pijamas', descripcion='Comoda y suave', precio=150,
                                        sku='530PA')
        self.assertIsNotNone(categoria1, 'No existe ningun dato')
        self.assertIsNotNone(prod1, 'No existe ningun dato')
        venta = Venta()
        venta.usuario = usr
        venta.fecha_hora = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        venta.nombre_factura = 'Francisco Apaza'
        venta.nit = '3123Fa'
        venta.total_vendido = 500
        venta.save()
        self.assertEqual(venta.total_vendido, 500, 'Los campos de ventas no son iguales')

    def test_cambiarEstadoVenta(self):
        usr = User()
        usr.last_name = 'Juan'
        usr.first_name = 'Ramon'
        usr.username = 'jramon5'
        usr.email = 'jramon@ex.com'
        usr.set_password('test')
        usr.save()
        self.assertIsNotNone(usr, 'El usuario no existe')
        categoria1 = Categoria.objects.create(nombre='Probandos')
        categoria1.save()

        prod1 = Producto.objects.create(nombre='Pijamas', descripcion='Comoda y suave', precio=150,
                                        sku='530PA')
        self.assertIsNotNone(categoria1, 'No existe ningun dato')
        self.assertIsNotNone(prod1, 'No existe ningun dato')
        venta = Venta()
        venta.usuario = usr
        venta.fecha_hora = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        venta.nombre_factura = 'Francisco Apaza'
        venta.nit = '3123Fa'
        venta.total_vendido = 500
        venta.save()

        self.assertEqual(venta.total_vendido, 500, 'Los campos de ventas no son iguales')
        self.assertEquals(venta.estado, -5, 'El estado no es iniciado')
        prod = {
            'cantidad': 1,
            'precio': 300,
            'id': prod1.id
        }
        listProd = []
        listProd.append(prod)

        venta2 = Venta.objects.filter(id=venta.id).first()
        venta2.crearCompra(listProd)
        self.assertEquals(venta2.estado, 0, 'El estado no es creado')
        movStock = Movimiento_Stock.objects.filter(id_producto__categoria=venta.id).first()
        self.assertIsNone(movStock, 'No es None')

    def test_crear_entrega_y_pago(self):
        usr = User()
        usr.last_name = 'Juan'
        usr.first_name = 'Ramon'
        usr.username = 'jramon5'
        usr.email = 'jramon@ex.com'
        usr.set_password('test')
        usr.save()
        self.assertIsNotNone(usr, 'El usuario no existe')
        categoria1 = Categoria.objects.create(nombre='Probandos')
        categoria1.save()

        prod1 = Producto.objects.create(nombre='Pijamas', descripcion='Comoda y suave', precio=150,
                                        sku='530PA')
        self.assertIsNotNone(categoria1, 'No existe ningun dato')
        self.assertIsNotNone(prod1, 'No existe ningun dato')
        venta = Venta()
        venta.usuario = usr
        venta.fecha_hora = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        venta.nombre_factura = 'Francisco Apaza'
        venta.nit = '3123Fa'
        venta.total_vendido = 500
        venta.save()

        self.assertEqual(venta.total_vendido, 500, 'Los campos de ventas no son iguales')
        self.assertEquals(venta.estado, -5, 'El estado no es iniciado')
        prod = {
            'cantidad': 1,
            'precio': 300,
            'id': prod1.id
        }
        listProd = []
        listProd.append(prod)

        venta2 = Venta.objects.filter(id=venta.id).first()
        venta2.crearCompra(listProd)
        self.assertEquals(venta2.estado, 0, 'El estado no es creado')

        newEntrega = Entregas()
        newEntrega.direccion_entrega = 'Av. Siempre Viva'
        newEntrega.latitud = '3123'
        newEntrega.longitud = '-39'
        newEntrega.id_venta = Venta.objects.filter(id=venta.id).first()
        newEntrega.save()

        newPago = Pagos()
        newPago.id_venta = Venta.objects.filter(id=venta.id).first()
        newPago.save()

        self.assertEquals(newPago.estado, 0, 'El estado no es pendiente')
        self.assertIsNotNone(newEntrega,'Los datos estan en None')

    def test_comprobante_enviado(self):
        usr = User()
        usr.last_name = 'Juan'
        usr.first_name = 'Ramon'
        usr.username = 'jramon5'
        usr.email = 'jramon@ex.com'
        usr.set_password('test')
        usr.save()
        self.assertIsNotNone(usr, 'El usuario no existe')
        categoria1 = Categoria.objects.create(nombre='Probandos')
        categoria1.save()

        prod1 = Producto.objects.create(nombre='Pijamas', descripcion='Comoda y suave', precio=150,
                                        sku='530PA')
        self.assertIsNotNone(categoria1, 'No existe ningun dato')
        self.assertIsNotNone(prod1, 'No existe ningun dato')
        venta = Venta()
        venta.usuario = usr
        venta.fecha_hora = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        venta.nombre_factura = 'Francisco Apaza'
        venta.nit = '3123Fa'
        venta.total_vendido = 500
        venta.save()

        self.assertEqual(venta.total_vendido, 500, 'Los campos de ventas no son iguales')
        self.assertEquals(venta.estado, -5, 'El estado no es iniciado')
        prod = {
            'cantidad': 1,
            'precio': 300,
            'id': prod1.id
        }
        listProd = []
        listProd.append(prod)

        venta2 = Venta.objects.filter(id=venta.id).first()
        venta2.crearCompra(listProd)
        venta2.save()
        self.assertEquals(venta2.estado, 0, 'El estado no es creado')

        newEntrega = Entregas()
        newEntrega.direccion_entrega = 'Av. Siempre Viva'
        newEntrega.latitud = '3123'
        newEntrega.longitud = '-39'
        newEntrega.id_venta = Venta.objects.filter(id=venta.id).first()
        newEntrega.save()

        newPago = Pagos()
        newPago.id_venta = Venta.objects.filter(id=venta.id).first()
        newPago.save()

        self.assertEquals(newPago.estado, 0, 'El estado no es pendiente')
        self.assertIsNotNone(newEntrega, 'Los datos estan en None')

        pagoReal = Pagos.objects.filter(id_venta_id=venta2.id).first()
        pagoReal.monto_pagado = 300
        pagoReal.subirPago(venta2.id)
        # pagoReal.save()

        self.assertEquals(pagoReal.estado, 1, 'El estado no es igual a PAGADO')

    def test_pago_aceptado(self):
        usr = User()
        usr.last_name = 'Juan'
        usr.first_name = 'Ramon'
        usr.username = 'jramon5'
        usr.email = 'jramon@ex.com'
        usr.set_password('test')
        usr.save()
        self.assertIsNotNone(usr, 'El usuario no existe')
        categoria1 = Categoria.objects.create(nombre='Probandos')
        categoria1.save()

        prod1 = Producto.objects.create(nombre='Pijamas', descripcion='Comoda y suave', precio=150,
                                        sku='530PA')
        self.assertIsNotNone(categoria1, 'No existe ningun dato')
        self.assertIsNotNone(prod1, 'No existe ningun dato')
        venta = Venta()
        venta.usuario = usr
        venta.fecha_hora = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        venta.nombre_factura = 'Francisco Apaza'
        venta.nit = '3123Fa'
        venta.total_vendido = 500
        venta.save()

        self.assertEqual(venta.total_vendido, 500, 'Los campos de ventas no son iguales')
        self.assertEquals(venta.estado, -5, 'El estado no es iniciado')
        prod = {
            'cantidad': 1,
            'precio': 300,
            'id': prod1.id
        }
        listProd = []
        listProd.append(prod)

        venta2 = Venta.objects.filter(id=venta.id).first()
        venta2.crearCompra(listProd)
        venta2.save()
        self.assertEquals(venta2.estado, 0, 'El estado no es creado')

        newEntrega = Entregas()
        newEntrega.direccion_entrega = 'Av. Siempre Viva'
        newEntrega.latitud = '3123'
        newEntrega.longitud = '-39'
        newEntrega.id_venta = Venta.objects.filter(id=venta.id).first()
        newEntrega.save()

        newPago = Pagos()
        newPago.id_venta = Venta.objects.filter(id=venta.id).first()
        newPago.save()

        self.assertEquals(newPago.estado, 0, 'El estado no es pendiente')
        self.assertIsNotNone(newEntrega, 'Los datos estan en None')

        pagoReal = Pagos.objects.filter(id_venta_id=venta2.id).first()
        pagoReal.monto_pagado = 300
        pagoReal.subirPago(venta2.id)
        # pagoReal.save()
        self.assertEquals(pagoReal.estado, 1, 'El estado no es igual a PAGADO')
        pagoReal.aprobarPago(pagoReal.id_venta_id)
        self.assertEquals(pagoReal.estado, 2, 'El estado no es igual a APROBADO')

    def test_pago_anulado(self):
        usr = User()
        usr.last_name = 'Juan'
        usr.first_name = 'Ramon'
        usr.username = 'jramon5'
        usr.email = 'jramon@ex.com'
        usr.set_password('test')
        usr.save()
        self.assertIsNotNone(usr, 'El usuario no existe')
        categoria1 = Categoria.objects.create(nombre='Probandos')
        categoria1.save()

        prod1 = Producto.objects.create(nombre='Pijamas', descripcion='Comoda y suave', precio=150,
                                        sku='530PA')
        self.assertIsNotNone(categoria1, 'No existe ningun dato')
        self.assertIsNotNone(prod1, 'No existe ningun dato')
        venta = Venta()
        venta.usuario = usr
        venta.fecha_hora = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        venta.nombre_factura = 'Francisco Apaza'
        venta.nit = '3123Fa'
        venta.total_vendido = 500
        venta.save()

        self.assertEqual(venta.total_vendido, 500, 'Los campos de ventas no son iguales')
        self.assertEquals(venta.estado, -5, 'El estado no es iniciado')
        prod = {
            'cantidad': 1,
            'precio': 300,
            'id': prod1.id
        }
        listProd = []
        listProd.append(prod)

        venta2 = Venta.objects.filter(id=venta.id).first()
        venta2.crearCompra(listProd)
        venta2.save()
        self.assertEquals(venta2.estado, 0, 'El estado no es creado')

        newEntrega = Entregas()
        newEntrega.direccion_entrega = 'Av. Siempre Viva'
        newEntrega.latitud = '3123'
        newEntrega.longitud = '-39'
        newEntrega.id_venta = Venta.objects.filter(id=venta.id).first()
        newEntrega.save()

        newPago = Pagos()
        newPago.id_venta = Venta.objects.filter(id=venta.id).first()
        newPago.save()

        self.assertEquals(newPago.estado, 0, 'El estado no es pendiente')
        self.assertIsNotNone(newEntrega, 'Los datos estan en None')

        pagoReal = Pagos.objects.filter(id_venta_id=venta2.id).first()
        pagoReal.monto_pagado = 300
        pagoReal.subirPago(venta2.id)
        # pagoReal.save()
        self.assertEquals(pagoReal.estado, 1, 'El estado no es igual a PAGADO')
        venta2.ventaAnulada2(venta2.id);
        self.assertEquals(venta2.estado, -2, 'El estado no es igual a ANULADO')
