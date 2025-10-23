# Modelo para tabela de filmes no banco de dados (cada classe = uma tabela no banco)

from datetime import datetime

from sqlalchemy import DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import table_registry

# Mapped -> mapeia o tipo mais próximo do banco (ex: str aqui = varchar lá)
# mapped_column -> entende automaticamente o contexto da classe e faz algumas configurações de mapeamento para dizer a coluna deve ser do tipo anotado em Mapped[...]


@table_registry.mapped_as_dataclass
class MovieModel:
    __tablename__ = 'filmes'

    id: Mapped[int] = mapped_column(
        primary_key=True, init=False
    )  # informa que o campo existe, mas não é algo que o usuário preenche manualmente na criação
    titulo: Mapped[str] = mapped_column(String(255))
    duracao: Mapped[str] = mapped_column(String(10))
    ano: Mapped[int]
    capa: Mapped[str] = mapped_column(String(255), unique=True)
    avaliacao_interna: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text('CURRENT_TIMESTAMP'), init=False
    )  # o banco guarda data do INSERT automaticamente, não é o usuário nem o python que preenche isso
    generos: Mapped[list['GeneroModel']] = relationship(
        secondary='genero_filme',  # nome da tabela intermediária
        back_populates='filmes',  # onde se conceta do outro lado (em GeneroModel)
    )
