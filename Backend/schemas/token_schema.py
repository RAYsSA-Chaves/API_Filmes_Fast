# Documentação do modelo dos dados do token para validação

from pydantic import BaseModel

# ---- Schema ----


class Token(BaseModel):
    type: str
    token: str
