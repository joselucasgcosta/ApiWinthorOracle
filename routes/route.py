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
    
@client_router.get("/aswer_table")
async def answer_table(codfilial: int, user: dict = Depends(get_current_user)):
    if codfilial <= 0:
        raise HTTPException(status_code=400, detail="Código inválido")
    try:
        result = Model.answer_table(codfilial)
        if not result:
            raise HTTPException(status_code=404, detail="Tabela não atualizada")
        return {
            "user": user["username"],
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ Erro na rota /answer_table na filial {codfilial}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@client_router.get("/sales_by_rca_between_dates")
async def sales_by_rca_between_dates(codusur: int, data1: str, data2: str, user: dict = Depends(get_current_user)):
    if codusur <= 0:
        raise HTTPException(status_code=400, detail="Código inválido")
    try:
        result = Model.sales_by_rca_between_dates(codusur, data1, data2)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado")
        return {
            "user": user["username"],
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ Erro na rota /sales_by_rca_between_dates: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@client_router.get("/sales_by_rca")
async def sales_by_rca(codusur: int, data1: str, user: dict = Depends(get_current_user)):
    if codusur <= 0:
        raise HTTPException(status_code=400, detail="Código inválido")
    try:
        result = Model.sales_by_rca(codusur, data1)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado")
        return {
            "user": user["username"],
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ Erro na rota /sales_by_rca: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
    
@client_router.get("/sales_by_superv_between_dates")
async def sales_by_superv_between_dates(codsuperv: int, data1: str, data2: str, user: dict = Depends(get_current_user)):
    if codsuperv <= 0:
        raise HTTPException(status_code=400, detail="Código inválido")
    try:
        result = Model.sales_by_superv_between_dates(codsuperv, data1, data2)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado")
        return {
            "user": user["username"],
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ Erro na rota /sales_by_superv_between_dates: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@client_router.get("/sales_by_superv")
async def sales_by_superv(codsuperv: int, data1: str, user: dict = Depends(get_current_user)):
    if codsuperv <= 0:
        raise HTTPException(status_code=400, detail="Código inválido")
    try:
        result = Model.sales_by_superv(codsuperv, data1)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado")
        return {
            "user": user["username"],
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ Erro na rota /sales_by_superv: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
    
@client_router.get("/promos")
async def promos(codfilial: int, condicoes: str, user: dict = Depends(get_current_user)):
    if codfilial <= 0:
        raise HTTPException(status_code=400, detail="Código inválido")
    try:
        result = Model.promos(codfilial, condicoes)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado")
        return {
            "user": user["username"],
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ Erro na rota /promos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@client_router.get("/nf_xml_data")
async def nf_xml_data(numnota: int, user: dict = Depends(get_current_user)):
    if numnota <= 0:
        raise HTTPException(status_code=400, detail="Código inválido")
    try:
        result = Model.nf_xml_data(numnota)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado")
        return {
            "user": user["username"],
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ Erro na rota /nf_xml_data: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@client_router.get("/boleto_data")
async def boleto_data(numnota: int, user: dict = Depends(get_current_user)):
    if numnota <= 0:
        raise HTTPException(status_code=400, detail="Código inválido")
    try:
        result = Model.boleto_data(numnota)
        return {
            "user": user["username"],
            "data": result or []
        }
    except Exception as e:
        logger.error(f"❌ Erro na rota /boleto_data: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")