# Documentação dos modelos dos dados para associação de gênero e filme para validação

from pydantic import BaseModel

# ---- Schemas ----


# para post de gênero + filme
class GeneroFilmeSchema(BaseModel):
    id_genero: int
    id_filme: int


# para listar todos as associações de gênero e filme
class GeneroFilmeList(BaseModel):
    genero_filme: list[GeneroFilmeSchema]
