from dao.pedidosDAO import PedidoDAO
from fastapi import APIRouter, Request, Depends
from models.PedidoModel import Item, PedidoInsert, PedidoPay, Salida, PedidosSalida, Comprador, Vendedor, PedidoSelect, \
    PedidoCancelacion, PedidoConfirmacion, PedidosSalidaID, RegistroEvento, ConsultaHistorial, PedidoEventos
from models.UsuariosModel import UsuarioSalida
from routers.usuariosRouter import validarUsuario

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post("/", response_model=Salida)
async def crearPedido(pedido: PedidoInsert, request: Request) -> Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.agregar(pedido)


@router.put("/")
async def modificarPedido():
    return {"mensaje": "Modificando un pedido"}


@router.delete("/{idPedido}/cancelar", summary="Cancelacion de un pedido", response_model=Salida)
async def eliminarPedido(idPedido: str, pedidoCancelacion: PedidoCancelacion, request: Request) -> Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.cancelarPedido(idPedido, pedidoCancelacion)


@router.get("/", response_model=PedidosSalida, response_description="Consulta de Pedidos")
async def consultaPedidos(request: Request, respuesta: UsuarioSalida = Depends(validarUsuario)) -> PedidosSalida:
    salida = PedidosSalida(estatus="", mensaje="", pedidos=[])
    usuario=respuesta.usuario
    if respuesta.estatus == 'OK' and usuario['tipo'] == 'Administrador':
        pedidoDAO = PedidoDAO(request.app.db)
        return pedidoDAO.consultaGeneral()
    else:
        salida.estatus = "ERROR"
        salida.mensaje = "Sin Auth"
        return salida


@router.put("/{idPedido}/agregarProducto")
async def agregarProductoPedido(idPedido: str, item: Item):
    salida = {"mensaje": "Agregando un producto al pedido: " + idPedido, "item: ": item.dict()}
    return salida


@router.put("/{idPedido}/pagar", summary="Pagar pedido", response_model=Salida)
async def pagarPedido(idPedido: str, pedidoPay: PedidoPay, request: Request):
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.pagarPedido(idPedido, pedidoPay)


# Práctica 1
@router.put("/{idPedido}/confirmar", response_model=Salida, summary="Confirmar un pedido pagado")
async def confirmarPedido(idPedido: str, pedidoConfirmacion: PedidoConfirmacion, request: Request) -> Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.confirmarPedido(idPedido, pedidoConfirmacion)


# Práctica 2
@router.get("/{idPedido}", response_model=PedidosSalidaID, summary="Consultar un pedido por su ID")
async def consultarPedidoID(idPedido: str, request: Request) -> PedidosSalidaID:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.consultarPedidoPorID(idPedido)


# EXAMEN - Registrar evento (POST)
@router.post("/{idPedido}/tracking", response_model=Salida, summary="Registrar evento de tracking")
async def registrar_evento(idPedido: str, evento: RegistroEvento, request: Request) -> Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.registrarEvento(idPedido, evento)


# EXAMEN - Consultar historial (GET)
@router.get("/{idPedido}/tracking", response_model=ConsultaHistorial, summary="Consultar historial de envío")
async def consultar_historial(idPedido: str, request: Request) -> ConsultaHistorial:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.consultarEventos(idPedido)
