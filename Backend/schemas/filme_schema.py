# Documentação dos modelos dos dados dos filmes para validação

from typing import Annotated, List
# Annotated = permite anexar informações extras a um tipo

from pydantic import AnyUrl, BaseModel, Field, StringConstraints

from .genero_schema import GeneroSchema

# ---- Tipos personalizados ----

# String com restrição para tempo de duraçãom (aceita "1h" ou "30min" ou "1h30min")
TempoStr = Annotated[str, StringConstraints(pattern=r'^(\d+h)?(\d+min)?$')]

# Float para nota do filme (máximo 10)
NotaMax = Annotated[float, Field(le=10)]


# ---- Schemas ----


# para teste
class MessageSchema(BaseModel):
    message: str


# para post de filme
class MovieSchema(BaseModel):
    titulo: str
    duracao: TempoStr
    ano: int
    capa: AnyUrl
    avaliacao_interna: NotaMax
    generos: List[int]  # lista de IDs dos gêneros


# retirando infos sigilosas da resposta das requisições
class MoviePublic(BaseModel):
    id: int
    titulo: str
    duracao: TempoStr
    ano: int
    capa: AnyUrl
    generos: List[GeneroSchema]


# para salvar no fake db
# class MovieDB(MovieSchema):
#     id: int


# para get de todos os filmes
class MovieList(BaseModel):
    filmes: list[MoviePublic]
