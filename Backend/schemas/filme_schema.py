# Documentação dos modelos dos dados dos filmes para validação


from typing import Annotated, List  # Annotated = permite anexar informações extras a um tipo

from pydantic import AnyUrl, BaseModel, EmailStr, Field, StringConstraints

from datetime import datetime

from models.filme_model import IndicativeRating

from .genero_schema import GeneroSchema


# ---- Tipos personalizados ----

# String com restrição para tempo de duraçãom (aceita '1h' ou '30min' ou '1h30min')
TempoStr = Annotated[str, StringConstraints(pattern=r'^(\d+h\d+min|\d+h|\d+min)$')]

# Float para nota do filme (máximo 10)
NotaMax = Annotated[float, Field(le=10)]


# ---- Schemas ----


# para teste
class MessageSchema(BaseModel):
    message: str


# para pegar email do usuário
class UserEmail(BaseModel):
    email: EmailStr

    model_config = {'from_attributes': True}


# filtros
class FilterPage(BaseModel):
    page: int = Field(1, ge=1, description='Número da página')
    limit: int = Field(10, ge=1, description='Número de filmes por página')

class FilterMovie(FilterPage):
    titulo: str | None = Field(default=None, max_length=20)
    ano: int | None = None
    genero: List[int] | None = None


# para post de filme
class MovieSchema(BaseModel):
    titulo: str
    duracao: TempoStr = Field(
        example='1h30min', description='Duração do filme (ex: 1h30min, 45min)'
    )  # infos para o Swagger
    ano: int = Field(example=2020)
    capa: AnyUrl
    avaliacao_interna: NotaMax
    generos: List[int]  # lista de IDs dos gêneros
    classificacao: IndicativeRating = Field(IndicativeRating.L)


# retirando infos sigilosas da resposta das requisições
class MoviePublic(BaseModel):
    id: int
    titulo: str
    duracao: TempoStr
    ano: int
    capa: AnyUrl
    generos: List[GeneroSchema]
    classificacao: IndicativeRating
    usuario: UserEmail
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}

    # model_config -> o FastAPI tenta acessar os campos como se fosse obj['id'], mas o SQLAlchemy trabalha com obj.id, isso gera erro, ele não consegue tranformar em json; essa configuração informa ao Pydantic que o modelo pode ser criado a partir de atributos de um objeto
    # “Pydantic, quando você receber um objeto (em vez de um dict), acesse seus atributos com ponto (obj.atributo) e monte o schema a partir disso.”


# para get de todos os filmes
class MovieList(BaseModel):
    filmes: list[MoviePublic]


# para patch
class MovieUpdate(BaseModel):
    titulo: str | None = None
    duracao: TempoStr | None = None
    ano: int | None = None
    capa: AnyUrl | None = None
    avaliacao_interna: NotaMax | None = None
    generos: List[int] | None = None
    classificacao: IndicativeRating | None = None


# para salvar no fake db
# class MovieDB(MovieSchema):
#     id: int