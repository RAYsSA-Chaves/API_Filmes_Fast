# Documentação dos modelos dos dados dos gêneros para validação

from pydantic import BaseModel

# ---- Schemas ----


# para post de gênero
class GeneroSchema(BaseModel):
    id: int
    genero: str


# para listar todos os gêneros
class GeneroList(BaseModel):
    generos: list[GeneroSchema]
