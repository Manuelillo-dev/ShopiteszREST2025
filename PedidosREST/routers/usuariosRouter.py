from fastapi import APIRouter

router=APIRouter(prefix="/Usuarios", tags=["Usuarios"])

@router.get("/usuarios/login")
async def loginUsuarios():
    return {"mensaje":"validando credenciales del usuario"}