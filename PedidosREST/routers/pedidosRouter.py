from fastapi import APIRouter

from models.PedidoModel import Item, PedidoInsert

router=APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/")
async def crearPedido(pedido:PedidoInsert):
    salida = {"mensaje": "Creando un pedido","pedido":pedido}
    return salida

@router.put("/")
async def modificarPedido():
    salida = {"mensaje":"Modificando pedido"}
    return salida

@router.delete("/")
async def eliminarPedido():
    salida = {"mensaje":"Eliminando pedido"}
    return salida

@router.get("/")
async def consultaPedidos():
    salida = {"mensaje": "Consultando los pedidos"}
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