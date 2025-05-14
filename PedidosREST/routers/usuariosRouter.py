from fastapi import APIRouter, Request
from models.UsuariosModel import Login, UsuarioSalida
from dao.usuariosDAO import UsuarioDAO

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/Autenticar", response_model = UsuarioSalida, summary="Autenticar un usuario")
async def login(login: Login, request: Request) -> UsuarioSalida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.autenticar(login.email, login.password)