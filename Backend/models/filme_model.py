# Modelo para tabela de filmes no banco de dados (cada classe = uma tabela no banco)

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from . import table_registry

# Mapped -> mapeia o tipo mais próximo do banco (ex: str aqui = varchar lá)
# mapped_column -> entende automaticamente o contexto da classe e faz algumas configurações de mapeamento para dizer a coluna deve ser do tipo anotado em Mapped[...]


@table_registry.mapped_as_dataclass
class MovieModel:
    __tablename__ = 'filmes'

    id: Mapped[int] = mapped_column(
        primary_key=True, init=False
    )  # informa que o campo existe, mas não é algo que o usuário preenche manualmente na criação
    titulo: Mapped[str]
    duracao: Mapped[str]
    ano: Mapped[int]
    capa: Mapped[str] = mapped_column(unique=True)
    avaliacao_interna: Mapped[float]
    created_at: Mapped[datetime]  # guardar data de cadastro
