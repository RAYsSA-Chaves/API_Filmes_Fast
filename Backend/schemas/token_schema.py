# Documentação do modelo dos dados do token para validação

from pydantic import BaseModel

# ---- Schema ----


class Token(BaseModel):
    access_token: str
    token_type: str
