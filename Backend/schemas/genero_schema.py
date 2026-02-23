# Documentação dos modelos dos dados dos gêneros para validação

from pydantic import BaseModel, field_validator, Field


# ---- Schemas ----

# para post de gênero
class GeneroCreate(BaseModel):
    genero: str


# para retorno dos gêneros
class GeneroSchema(BaseModel):
    id: int
    genero: str = Field(min_length=3, max_length=30)

    # validações
    @field_validator('genero')
    @classmethod
    def genero_nao_vazio(cls, value):
        if value.strip() == '':
            raise ValueError('O nome do gênero não pode ser vazio.')
        return value.strip()

    model_config = {'from_attributes': True}


# listar todos os gêneros
class GeneroList(BaseModel):
    generos: list[GeneroSchema]