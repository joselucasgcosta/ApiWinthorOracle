from fastapi import APIRouter, HTTPException, Depends
from security.auth import get_current_user
from fastapi.responses import JSONResponse
from logger.setup_logger import setup_logger, get_logger
from models.model import Model

# Configura o logger
setup_logger()
logger = get_logger(__name__)

client_router = APIRouter()

@client_router.get("/client")
async def get_info_client(codcli: int, user: dict = Depends(get_current_user)):
    if codcli <= 0:
        raise HTTPException(status_code=400, detail="Código inválido")
    try:
        result = Model.query_info_client(codcli)
        if not result:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return {
            "user": user["username"],
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ Erro na rota /client para codcli={codcli}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")