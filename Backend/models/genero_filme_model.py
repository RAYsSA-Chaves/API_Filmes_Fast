# Modelo para tabela de associação de gêneros e filmes no banco de dados

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from . import table_registry


@table_registry.mapped_as_dataclass
class GeneroFilmeModel:
    __tablename__ = 'genero_filme'

    id_filme: Mapped[int] = mapped_column(ForeignKey('filmes.id'), primary_key=True)
    id_genero: Mapped[int] = mapped_column(ForeignKey('generos.id'), primary_key=True)
