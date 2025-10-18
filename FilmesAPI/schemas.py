# Documentação dos modelos dos dados para validação

from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str
