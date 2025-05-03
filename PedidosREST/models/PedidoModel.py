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
    motivoCancelacion: str

class detalle(BaseModel):
    idProducto: int
    cantidad: int

class Envio(BaseModel):
    fechaSalida: datetime
    fechaEntPlan: datetime
    noGuia: str
    idPaqueteria: int
    detalle: list[detalle]

#Práctica 1
class PedidoConfirmacion(BaseModel):
    fechaConfirmacion: datetime | None = None
    estatus: str | None = "Confirmado"
    envio: Envio

#Práctica 2
class Items(BaseModel):
    idProducto: int
    nombreProducto: str #Se agrega un extra de "Item", el cual será útil en la entrada y salida
    cantidad: int
    precio: float
    subtotal: float
    costoEnvio: float
    subtotalEnvio: float

class Pago2(BaseModel):
    idTarjeta: int | None = None     #Diferenciando el primer pago
    noTarjeta: str
    fecha: datetime
    monto: float
    estatus: str

class Paqueteria(BaseModel):
    idPaqueteria: int
    nombre: str | None = None

class Envio2(BaseModel):    #Aquí se omite detalle y en paqueteria se agrego por la auscencia del nombre
    fechaSalida: datetime
    fechaEntPlan: datetime
    fechaRecepcion: datetime | None = None #Omitido, tampoco lo tiene
    noGuia: str
    paqueteria: Paqueteria | None = None

class Productos(BaseModel):
    idProducto: int
    nombreProducto: str
    cantidadEnviada: int
    cantidadRecibida: int | None = None
    comentario: str | None = None

class PedidoSelectID(BaseModel):
    idPedido: str
    fechaRegistro: datetime
    fechaConfirmacion: datetime | None = None
    fechaCierre: datetime | None = None
    costosEnvio: float
    subtotal: float
    totalPagar: float
    estatus: str
    motivoCancelacion: str | None = None
    valoracion: int | None = None
    items: list[Items]
    pago: Pago2
    comprador: Comprador
    vendedor: Vendedor
    envio: Envio2
    productos: list[Productos]
    paqueteria: Paqueteria

class PedidosSalidaID(Salida):
    pedido: PedidoSelectID | None = None