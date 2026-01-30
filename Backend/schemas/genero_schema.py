# Documentação dos modelos dos dados dos gêneros para validação

from pydantic import BaseModel


# ---- Schemas ----


# para post de gênero
class GeneroCreate(BaseModel):
    genero: str


# para retorno dos gêneros
class GeneroSchema(BaseModel):
    id: int
    genero: str
    model_config = {'from_attributes': True}


# para listar todos os gêneros
class GeneroList(BaseModel):
    generos: list[GeneroSchema]
