from fastapi import APIRouter
import datetime
from models.PedidoModel import Item, PedidoInsert, DatosPago, Salida, PedidosSalida, PedidoSelect, Vendedor,Comprador

router=APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/",response_model=Salida)
async def crearPedido(pedido:PedidoInsert)->Salida:
    salida = Salida(estatus='OK', mensaje='Pedido creado con exito')
    #return = {"mensaje": "Creando un pedido","pedido":pedido}
    return  salida

@router.put("/")
async def modificarPedido():
    salida = {"mensaje":"Modificando pedido"}
    return salida

@router.delete("/")
async def eliminarPedido():
    salida = {"mensaje":"Eliminando pedido"}
    return salida

@router.get("/",response_model=PedidosSalida)
async def consultaPedidos()->PedidosSalida:
    comprador=Comprador(idComprador=1,nombre="Juan")
    vendedor=Vendedor(idVendedor=1, nombre="Walmart")
    pedido=PedidoSelect(idPedido="500",fechaRegistro=datetime.date.today(),
                        fechaConfirmacion=datetime.date.today(),
                        fechaCierre=datetime.date.today(),
                        costosEnvio=100, subtotal=200,totalPagar=3000,estatus="Pagado",
                        comprador=comprador, vendedor=vendedor)
    lista=[]
    lista.append(pedido)
    salida=PedidosSalida(estatus="OK", mensaje="Consulta de Pedidos",pedidos=lista)
    #salida = {"mensaje": "Consultando los pedidos"}
    return salida

@router.get("/{idPedido}")
async def consultarPedido(idPedido:str):
    salida = {"mensaje": "Consultando el pedido: " + idPedido}
    return salida

@router.put("/{idPedido}/agregarProducto")
async def agregarProductoPedido(idPedido:str,item:Item):
    salida = {"mensaje": "Agregando un producto al pedido: " + idPedido ,"item": item.dict()}
    return salida

@router.put("/{idPedido}/pagarPedido")
async def pagarPedido(idPedido:str,item:Item):
    salida = {"mensaje": "Agregando pago del producto: ","item": item.dict()}
    return salida