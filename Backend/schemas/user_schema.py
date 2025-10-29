# Documentação dos modelos dos dados dos usuários para validação

from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


# ---- Tipos personalizados ----

SenhaStr = Annotated[str, Field(min_length=6)]

# ---- Schemas ----

# para cadastro
class UserCreate(BaseModel):
    email: EmailStr
    senha: SenhaStr

# retirando infos sigilosas da resposta das requisições (senha)
class UserPublic(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True} 