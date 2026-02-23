# Documentação dos modelos dos dados dos filmes para validação

from typing import Annotated, List  # Annotated permite anexar informações extras a um tipo
from pydantic import AnyUrl, BaseModel, EmailStr, Field, StringConstraints, field_serializer, field_validator
from datetime import datetime
from models.filme_model import IndicativeRating
from .genero_schema import GeneroSchema
from .user_schema import UserEmail


# ---- Tipos personalizados ----

# String com restrição para tempo de duração (aceita '1h' ou '30min' ou '1h30min')
TempoStr = Annotated[str, StringConstraints(pattern=r'^(\d+h\d+min|\d+h|\d+min)$')]

# Float para nota do filme (máximo 10)
NotaMax = Annotated[float, Field(ge=0, le=10)]


# ---- Schemas ----

# mensagem básica
class MessageSchema(BaseModel):
    message: str


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
    titulo: str = Field(min_length=1)
    duracao: TempoStr = Field(
        example='1h30min', 
        description='Duração do filme (ex: 1h30min, 45min)'
    )  # infos para o Swagger
    ano: int = Field(example=2020, ge=1888)
    capa: AnyUrl
    avaliacao_interna: NotaMax
    generos: List[int]  # lista de IDs dos gêneros
    classificacao: IndicativeRating = IndicativeRating.L

    # validações
    @field_validator('titulo')
    @classmethod
    def titulo_nao_vazio(cls, value):
        if value.strip() == '':
            raise ValueError('O título não pode ser vazio.')
        return value
    
    @field_validator('generos')
    @classmethod
    def generos_nao_vazio(cls, value):
        if len(value) == 0:
            raise ValueError('É obrigatório informar pelo menos um gênero para o filme.')
        return value


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

    # classificação deve retornar o texto completo nas respostas das requisições
    @field_serializer('classificacao')
    def serialize_classificacao(self, value):
        return value.label

    # model_config -> o FastAPI tenta acessar os campos como se fosse obj['id'], mas o SQLAlchemy trabalha com obj.id, isso gera erro; essa configuração informa ao Pydantic que o modelo pode ser criado a partir de atributos de um objeto
    # “Pydantic, quando você receber um objeto (em vez de um dict), acesse seus atributos com ponto (obj.atributo) e monte o schema a partir disso.”


# para get de todos os filmes
class MovieList(BaseModel):
    filmes: list[MoviePublic]


# para patch
class MovieUpdate(BaseModel):
    titulo: str | None = None
    duracao: TempoStr | None = Field(
        default=None,
        example='1h30min', 
        description='Duração do filme (ex: 1h30min, 45min)'
    )
    ano: int | None = None
    capa: AnyUrl | None = None
    avaliacao_interna: NotaMax | None = None
    generos: List[int] | None = None
    classificacao: IndicativeRating | None = None

    # validações 
    @field_validator('titulo')
    @classmethod
    def titulo_patch_nao_vazio(cls, value):
        if value is not None and value.strip() == '':
            raise ValueError('O título não pode ser vazio.')
        return value

    @field_validator('generos')
    @classmethod
    def generos_patch_nao_vazio(cls, value):
        if value is not None and len(value) == 0:
            raise ValueError('É obrigatório informar pelo menos um gênero para o filme.')
        return value


# para salvar no fake db
# class MovieDB(MovieSchema):
#     id: int