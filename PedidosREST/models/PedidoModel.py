from pydantic import BaseModel
from datetime import datetime

class Item(BaseModel):
    idProducto: int
    cantidad: int
    precio: float
    subtotal: float
    costoEnvio: float
    subtotalEnvio: float

class PedidoInsert(BaseModel):
    idComprador : int
    idVendedor: int
    costosEnvio: float
    subtotal: float
    total: float
    estatus: str | None = 'Captura'
    fechaRegistro: datetime | None = datetime.today()
    detalle: list[Item]

class Pago(BaseModel):
    fecha: datetime
    monto: float
    noTarjeta: str
    estatus: str

class PedidoPay(BaseModel):
    estatus: str | None = 'Pagado'
    pago:Pago

class Salida(BaseModel):
    estatus: str
    mensaje: str

class Comprador(BaseModel):
    idComprador: int
    nombre: str

class Vendedor(BaseModel):
    idVendedor: int
    nombre: str

class PedidoSelect(BaseModel):
    idPedido: str
    fechaRegistro: datetime
    fechaConfirmacion: datetime | None = None
    fechaCierre: datetime | None = None
    costosEnvio: float
    subtotal: float
    totalPagar: float
    estatus: str
    motivoCancelacion: str | None= None
    valoracion: int | None = None
    comprador: Comprador
    vendedor: Vendedor

class PedidosSalida(Salida):
    pedidos: list[PedidoSelect]

class PedidoCancelacion(BaseModel):
    motivoCancelacion:str

#Practica 1
class DetalleEnvio(BaseModel):
    idProducto: int
    cantidadEnviada: int

class Envio(BaseModel):
    fechaSalida: datetime
    fechaEntPlan: datetime
    noGuia: str
    idPaqueteria: int
    detalle: list[DetalleEnvio]

class PedidoConfirmar(BaseModel):
    fechaConfirmacion: datetime
    estatus: str | None = 'Confirmado'
    envio: Envio

