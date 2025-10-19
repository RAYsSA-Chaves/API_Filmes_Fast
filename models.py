# Modelo para o banco de dados (cada classe = uma tabela no banco)

from sqlalchemy.orm import Mapped, registry, mapped_column
from datetime import datetime
# Mapped -> mapeia o tipo mais próximo do banco (ex: str aqui = varchar lá)
# registry -> registra tudo o que será uma tabela no banco 
# mapped_column -> entende automaticamente o contexto da classe e faz algumas configurações de mapeamento para dizer que um campo deve estar associado ao tipo anotado em Mapped[...]

table_registry = registry()

@table_registry.mapped_as_dataclass
class MovieModel:
    __tablename__ = 'filmes'
    id: Mapped[int] = mapped_column(primary_kry=True, init=False) # informa que o campo existe, mas não é algo que o usuário precisa (ou pode) preencher manualmente na criação
    titulo: Mapped[str]
    duracao: Mapped[str]
    ano: Mapped[int]
    capa: Mapped[str] = mapped_column(unique=True)
    avaliacao_interna: Mapped[float]
    created_at: Mapped[datetime] # guardar data de cadastro