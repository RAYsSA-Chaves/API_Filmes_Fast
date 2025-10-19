# Modelo para tabela de gêneros no banco de dados

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from . import table_registry


@table_registry.mapped_as_dataclass
class GeneroModel:
    __tablename__ = 'generos'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    genero: Mapped[str]
    created_at: Mapped[datetime]
