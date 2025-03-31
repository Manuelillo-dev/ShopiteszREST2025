from datetime import datetime, date

from pydantic import BaseModel

class Item(BaseModel):
    idProducto:int
    cantidad:int
    precio:float
    subtotal:float
    costoEnvio:float
    subtotalEnvio:float

class PedidoInsert(BaseModel):
    idComprador:int
    idVendedor:int
    costoEnvio:float
    subtotal:float
    total:float
    estatus:str| None='Captura'
    detalle:list[Item]

class DatosPago(BaseModel):
    fecha:date|None=datetime.today()
    monto:float
    noTarjeta:str
    estatus:str

class PedidoPagar(BaseModel):
    estatus:str|None='Pagado'
    pago: DatosPago

class Salida(BaseModel):
    estatus:str
    mensaje: str

class Comprador(BaseModel):
    idComprador:int
    nombre:str

class Vendedor(BaseModel):
    idVendedor:int
    nombre:str

class PedidoSelect(BaseModel):
    idPedido:str
    fechaRegistro:date
    fechaConfirmacion:date
    fechaCierre:date
    costosEnvio:float
    subtotal:float
    totalPagar:float
    estatus:str
    motivoCancelacion:str|None=None
    valoracion:int|None=None
    comprador:Comprador
    vendedor:Vendedor

class PedidosSalida(Salida):
    pedidos:list[PedidoSelect]