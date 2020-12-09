from outime.models.producto import Producto


class SimplificadorDetalle:

    @staticmethod
    def crearDetalle(producto, id):
        from outime.models.detalle_venta import DetalleVenta
        detalle_venta = DetalleVenta()
        detalle_venta.cantidad_vendida = int(producto['cantidad'])
        detalle_venta.precio_venta = producto['precio']
        detalle_venta.producto = Producto.objects.filter(id=producto['id']).first()
        detalle_venta.venta_id = id
        detalle_venta.save()
        SimplificadorDetalle.movimientoStockNegativo(id, producto['id'], producto['cantidad'])

    @staticmethod
    def movimientoStockPositivo(idVenta, idProducto, cantidad):
        from outime.models.movimiento_stock import Movimiento_Stock
        mov_stock = Movimiento_Stock()
        mov_stock.id_producto = Producto.objects.filter(id=idProducto).first()
        from outime.models.ventas import Venta
        mov_stock.id_referencia = Venta.objects.filter(id=idVenta).first()
        mov_stock.cantidad = cantidad
        mov_stock.incrementarValor()
        mov_stock.save()

    @staticmethod
    def movimientoStockNegativo(idVenta, idProducto, cantidad):
        from outime.models.movimiento_stock import Movimiento_Stock
        mov_stock = Movimiento_Stock()
        mov_stock.id_producto = Producto.objects.filter(id=idProducto).first()
        from outime.models.ventas import Venta
        mov_stock.id_referencia = Venta.objects.filter(id=idVenta).first()
        mov_stock.cantidad = int(cantidad) * -1
        mov_stock.save()

    @staticmethod
    def cambioPendientePago(idVenta):
        from outime.models.ventas import Venta
        ventaRealizada = Venta.objects.filter(id=idVenta).first()
        ventaRealizada.pagar()
        ventaRealizada.save()

    @staticmethod
    def aprobadoPago(idVenta):
        from outime.models.ventas import Venta
        ventaRealizada = Venta.objects.filter(id=idVenta).first()
        ventaRealizada.pagoAceptado()
        ventaRealizada.save()

    @staticmethod
    def pagoAnulado(idVenta):
        from outime.models.detalle_venta import DetalleVenta
        detalleVenta = DetalleVenta.objects.filter(id=idVenta).all()
        for x in detalleVenta:
            SimplificadorDetalle.movimientoStockPositivo(idVenta, x.producto.id, x.cantidad_vendida)
        from outime.models.ventas import Venta
        ventaRealizada = Venta.objects.filter(id=idVenta).first()
        ventaRealizada.pagoRechazado()
        ventaRealizada.save()

    @staticmethod
    def ventaAnulada(idVenta):
        from outime.models.detalle_venta import DetalleVenta
        detalleVenta = DetalleVenta.objects.filter(id=idVenta).all()
        for x in detalleVenta:
            SimplificadorDetalle.movimientoStockPositivo(idVenta, x.producto.id, x.cantidad_vendida)
        from outime.models.pagos import Pagos
        pagoRealizado = Pagos.objects.filter(id_venta_id=idVenta).first()
        pagoRealizado.anularPago2()
        pagoRealizado.save()

    @staticmethod
    def ventaAnulada(idVenta):
        from outime.models.detalle_venta import DetalleVenta
        detalleVenta = DetalleVenta.objects.filter(id=idVenta).all()
        [SimplificadorDetalle.movimientoStockPositivo(idVenta, i.producto.id, i.cantidad_vendida) for i in detalleVenta]
        from outime.models.pagos import Pagos
        pagoRealizado = Pagos.objects.filter(id_venta_id=idVenta).first()
        pagoRealizado.anularPago2()
        pagoRealizado.save()
