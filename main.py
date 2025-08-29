from fastapi import FastAPI
from routes.route import client_router
from routes.token import token_router

app = FastAPI()

# Inclui o router com prefixo e tags
app.include_router(token_router, tags=["Autenticação"])
app.include_router(client_router, prefix="/info", tags=["Cliente"])
