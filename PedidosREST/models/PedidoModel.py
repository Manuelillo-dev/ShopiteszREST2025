from datetime import datetime

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
    fecha:datetime
    monto:float
    noTarjeta:str
    estatus:str

class PedidoPagar(BaseModel):
    estatus: str
    pago: list[DatosPago]