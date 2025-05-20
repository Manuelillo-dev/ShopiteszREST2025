from ctypes.wintypes import HHOOK

from fastapi import APIRouter, Request, Depends
from models.UsuariosModel import Login, UsuarioSalida
from dao.usuariosDAO import UsuarioDAO
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

security = HTTPBasic()


@router.post("/Autenticar", response_model=UsuarioSalida, summary="Autenticar un usuario")
async def login(login: Login, request: Request) -> UsuarioSalida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.autenticar(login.email, login.password)


async def validarUsuario(request:Request, credenciales: HTTPBasicCredentials=Depends(security))-> UsuarioSalida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.autenticar(credenciales.username, credenciales.password)


