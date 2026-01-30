# Documentação dos modelos dos dados dos filmes para validação

# Annotated = permite anexar informações extras a um tipo
from typing import Annotated, List

from pydantic import AnyUrl, BaseModel, Field, StringConstraints, EmailStr

from .genero_schema import GeneroSchema

from models.filme_model import IndicativeRating

# ---- Tipos personalizados ----

# String com restrição para tempo de duraçãom (aceita '1h' ou '30min' ou '1h30min')
TempoStr = Annotated[str, StringConstraints(pattern=r'^(\d+h\d+min|\d+h|\d+min)$')]

# Float para nota do filme (máximo 10)
NotaMax = Annotated[float, Field(le=10)]


# ---- Schemas ----


# para teste
class MessageSchema(BaseModel):
    message: str


# para pegar email da tabela de usuário
class UserEmail(BaseModel):
    email: EmailStr

    model_config = {'from_attributes': True}


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
    created_by: UserEmail

    model_config = {'from_attributes': True}


    # model_config -> o FastAPI tenta acessar os campos como se fosse obj['id'], mas o SQLAlchemy trabalha com obj.id, isso gera erro, ele não consegue tranformar em json; essa configuração informa ao Pydantic que o modelo pode ser criado a partir de atributos de um objeto
    # “Pydantic, quando você receber um objeto (em vez de um dict), acesse seus atributos com ponto (obj.atributo) e monte o schema a partir disso.”


# para salvar no fake db
# class MovieDB(MovieSchema):
#     id: int


# para get de todos os filmes
class MovieList(BaseModel):
    filmes: list[MoviePublic]
