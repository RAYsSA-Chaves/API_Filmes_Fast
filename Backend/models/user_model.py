# Modelo para tabela de usuários no banco de dados

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .filme_model import MovieModel

from . import table_registry


@table_registry.mapped_as_dataclass
class UserModel:
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    filmes_cadastrados: Mapped[list['MovieModel']] = relationship(
        back_populates='usuario',
        init=False,
    )
