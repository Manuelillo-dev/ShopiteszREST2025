from models.PedidoModel import PedidoInsert, Salida, PedidosSalida, PedidoPay, PedidoCancelacion, PedidoConfirmacion, \
    PedidoSelectID, PedidosSalidaID, RegistroEvento, ConsultaHistorial, EventoDetalle, EnvioPedido, PedidoEventos
from datetime import datetime
from dao.usuariosDAO import UsuarioDAO
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


class PedidoDAO:
    def __init__(self, db):
        self.db = db

    def agregar(self, pedido: PedidoInsert):
        salida = Salida(estatus="", mensaje="")
        try:
            pedido.fechaRegistro = datetime.today()
            if pedido.idVendedor != pedido.idComprador:
                usuarioDAO = UsuarioDAO(self.db)
                if usuarioDAO.comprobarUsuario(pedido.idComprador) and usuarioDAO.comprobarUsuario(pedido.idVendedor):
                    result = self.db.pedidos.insert_one(jsonable_encoder(pedido))
                    salida.estatus = "OK"
                    salida.mensaje = "Pedido agregado con exito con id: " + str(result.inserted_id)
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "El usuario comprador o el vendedor no existen o no se encuentran activos."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se pudo agregar el pedido, porque los ids de los usuarios son iguales."
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al agregar el pedido, consulta al adminstrador."
        return salida

    def consultaGeneral(self):
        salida = PedidosSalida(estatus="", mensaje="", pedidos=[])
        try:
            lista = list(self.db.pedidosView.find())
            salida.estatus = "OK"
            salida.mensaje = "Listado de pedidos."
            salida.pedidos = lista
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consulta los pedidos, consulta al adminstrador."
        return salida

    def evaluarPedido(self, idPedido: str):
        pedido = None
        try:
            pedido = self.db.pedidosView.find_one({"idPedido": idPedido, "estatus": "Captura"})
        except Exception as ex:
            print(ex)
        return pedido

    def pagarPedido(self, idPedido: str, pedidoPay: PedidoPay):
        salida = Salida(estatus="", mensaje="")
        try:
            pedido = self.evaluarPedido(idPedido)
            if pedido:
                usuarioDAO = UsuarioDAO(self.db)
                if usuarioDAO.comprobarTarjeta(pedido['comprador'].get("idComprador"), pedidoPay.pago.noTarjeta) == 1:
                    if pedido['total'] == pedidoPay.pago.monto and pedidoPay.pago.estatus == "Autorizado":
                        pedidoPay_dict = pedidoPay.dict()
                        pedidoPay_dict["estatus"] = "Pagado"
                        self.db.pedidos.update_one(
                            {"_id": ObjectId(idPedido)},
                            {"$set": {
                                "pago": pedidoPay_dict["pago"],
                                "estatus": pedidoPay_dict["estatus"]
                            }}
                        )
                        salida.estatus = "OK"
                        salida.mensaje = f"El pedido con id: {idPedido} fue pagado con exito"
                    else:
                        salida.estatus = "ERROR"
                        salida.mensaje = "El pedido no se puede pagar debido a que no se cubre el monto total a pagar"
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "El pedido no se puede pagar debido a que la tarjeta no existe o no pertenece al comprador"
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El pedido no existe o no se encuentra en captura"
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al pagar el pedido, consulta al adminstrador"
        return salida

    def cancelarPedido(self, idPedido: str, pedidoCancelacion: PedidoCancelacion):
        salida = Salida(estatus="", mensaje="")
        try:
            objeto = self.consultarEstatusPedido(idPedido)
            if objeto["estatus"] == "Captura":
                self.db.pedidos.update_one({"idPedido": idPedido},
                                           {"$set": {"estatus": "Cancelado",
                                                     "motivoCancelacion": pedidoCancelacion.motivoCancelacion}})
                salida.estatus = "OK"
                salida.mensaje = "Pedido cancelado con exito"
            elif objeto["estatus"] == "Pagado":
                self.db.pedidos.update_one({"idPedido": idPedido},
                                           {"$set": {"estatus": "Devolucion",
                                                     "motivoCancelacion": pedidoCancelacion.motivoCancelacion}})
                salida.estatus = "OK"
                salida.mensaje = "Se ha iniciado el proceso de reembolso"
            else:
                salida.estatus = "OK"
                salida.mensaje = "El pedido no existe o no se encuentran en Captura / Pagado"
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "El pedido no se puede cancelar, consulta al adminstrador."
        return salida

    # Práctica 1
    def confirmarPedido(self, idPedido: str, pedidoConfirmacion: PedidoConfirmacion) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            pedido = self.db.pedidos.find_one({"_id": ObjectId(idPedido)})
            if not pedido:
                salida.estatus = "ERROR"
                salida.mensaje = f"Pedido con id {idPedido} no encontrado."
                return salida
            if pedido["estatus"] != "Pagado":
                salida.estatus = "ERROR"
                salida.mensaje = f"El pedido debe estar en estatus Pagado. Estatus actual: {pedido.get('estatus')}"
                return salida
            if 'detalle' not in pedido:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontró el detalle del pedido."
                return salida
            detalle_pedido = {item['idProducto']: item['cantidad'] for item in pedido['detalle']}
            for envioItem in pedidoConfirmacion.envio.detalle:
                if envioItem.idProducto not in detalle_pedido:
                    salida.estatus = "ERROR"
                    salida.mensaje = f"Producto con id {envioItem.idProducto} no encontrado en el pedido original."
                    return salida
                if envioItem.cantidad != detalle_pedido.get(envioItem.idProducto):
                    salida.estatus = "ERROR"
                    salida.mensaje = f"La cantidad enviada ({envioItem.cantidad}) para el producto {envioItem.idProducto} no coincide con la cantidad pedida ({detalle_pedido.get(envioItem.idProducto)})."
                    return salida
            update_data = {
                "$set": {
                    "fechaConfirmacion": datetime.now(),
                    "estatus": "Confirmado",
                    "envio": jsonable_encoder(pedidoConfirmacion.envio)
                }
            }
            result = self.db.pedidos.update_one({"_id": ObjectId(idPedido)}, update_data)
            if result.modified_count > 0:
                salida.estatus = "OK"
                salida.mensaje = f"Pedido con id: {idPedido} confirmado con éxito."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = f"No se pudo confirmar el pedido con id: {idPedido}. (Puede que ya estuviera confirmado o no se encontró)."
        except Exception as ex:
            print(f"Error al confirmar el pedido {idPedido}: {ex}")
            salida.estatus = "ERROR"
            salida.mensaje = "Error al confirmar el pedido, consulta al administrador."
        return salida

    # Práctica 2
    def consultarPedidoPorID(self, idPedido: str) -> PedidosSalidaID:
        salida = PedidosSalidaID(estatus="", mensaje="", pedido=None)
        try:
            pedido_data = self.db.viewConsultaID.find_one({"idPedido": idPedido})
            if pedido_data:
                salida.pedido = pedido_data
                salida.estatus = "OK"
                salida.mensaje = f"Pedido {idPedido} encontrado con extito."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = f"El pedido con id {idPedido} no se ha encontrado."
        except Exception as e:
            print(f"Error al consultar el pedido {idPedido}: {e}")
            salida.estatus = "ERROR"
            salida.mensaje = "Error interno al consultar el pedido."
        return salida

    # EXAMEN - Metodo para registrar evento (POST)
    def registrarEvento(self, idPedido: str, evento: RegistroEvento) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            pedido = self.db.pedidos.find_one({"_id": ObjectId(idPedido)})

            # Validaciones
            if not pedido:
                salida.estatus = "ERROR"
                salida.mensaje = f"Pedido {idPedido} no encontrado"
                return salida

            if pedido.get("estatus") != "Confirmado":
                salida.estatus = "ERROR"
                salida.mensaje = "El pedido debe estar en estatus 'Confirmado'"
                return salida

            if "envio" not in pedido:
                salida.estatus = "ERROR"
                salida.mensaje = "El pedido no tiene información de envío"
                return salida

            # Actualizar pedido en MongoDB
            result = self.db.pedidos.update_one(
                {"_id": ObjectId(idPedido)},
                {"$push": {"envio.tracking": jsonable_encoder(evento)}}
            )

            if result.modified_count > 0:
                salida.estatus = "OK"
                salida.mensaje = f"Evento registrado en pedido {idPedido}"
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se pudo registrar el evento"

        except Exception as ex:
            print(f"Error al registrar evento: {ex}")
            salida.estatus = "ERROR"
            salida.mensaje = "Error interno al registrar evento"

        return salida

    # EXAMEN - Metodo para consultar historial (GET)
    def consultarEventos(self, idPedido: str) -> ConsultaHistorial:
        salida = ConsultaHistorial(estatus="", mensaje="", pedido=None)
        try:
            # 1. Validación rápida de estado (ahora redundante porque la vista ya filtra)
            pedido_status = self.db.pedidos.find_one(
                {"_id": ObjectId(idPedido)},
                {"estatus": 1}
            )

            if not pedido_status or pedido_status.get("estatus") != "Confirmado":
                salida.estatus = "ERROR"
                salida.mensaje = "El pedido no existe o no está Confirmado"
                return salida

            # 2. Consulta SIMPLE usando la vista (toda la lógica compleja está en MongoDB)
            pedido_data = self.db.viewHistorialEnvios.find_one(
                {"idPedido": idPedido}
            )

            if not pedido_data:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontró historial para el pedido"
                return salida

            # 3. Construcción de respuesta
            salida.estatus = "OK"
            salida.mensaje = "Consulta exitosa"
            salida.pedido = {
                "idPedido": pedido_data["idPedido"],
                "envio": {
                    "idPaqueteria": pedido_data["idPaqueteria"],
                    "paqueteria": pedido_data.get("nombrePaqueteria", "Sin especificar"),
                    "noGuia": pedido_data["noGuia"],
                    "tracking": pedido_data["tracking"]
                }
            }

        except Exception as ex:
            print(f"Error al consultar eventos: {str(ex)}")
            salida.estatus = "ERROR"
            salida.mensaje = "Error interno al consultar historial"

        return salida
