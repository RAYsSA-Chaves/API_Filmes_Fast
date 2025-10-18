# Documentação dos modelos dos dados para validação

from typing import Annotated  # permite anexar informações extras a um tipo

from pydantic import AnyUrl, BaseModel, Field, StringConstraints

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


# retirando infos sigilosas da resposta das requisições
class MoviePublic(BaseModel):
    id: int
    titulo: str
    duracao: TempoStr
    ano: int
    capa: AnyUrl


# para salvar no fake db
class MovieDB(MovieSchema):
    id: int


# para get de todos os filmes
class MovieList(BaseModel):
    filmes: list[MoviePublic]
