from fastapi import FastAPI

from api.v1.routes import filmes, generos, root
from core.config import settings

app = FastAPI(title='Minha API de filmes 🎬')


# Incluir as rotas criadas
app.include_router(root.router, prefix=settings.API_V1_STR)
app.include_router(filmes.router, prefix=settings.API_V1_STR)
app.include_router(generos.router, prefix=settings.API_V1_STR)