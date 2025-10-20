# Configurando a conexão com o banco (cria o mecanismo/engine e sessão assíncrona do SQLAlchemy)

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

# AsyncEngine = tipo
# AsyncSession = classe pai, permite usar await
# sessionmaker = fábrica de sessões

# Engine
engine: AsyncEngine = create_async_engine(settings.DB_URL)

# Fábrica de sessões para criar várias sessions depois
Session: AsyncEngine = sessionmaker(
    autocommit=False,  # não faz commit automaticamente, precisa de await session.commit() para salvar alterações
    autoflush=False,  # não envia alterações pendentes automaticamente
    expire_on_commit=False,  # mantém os valores na memória mesmo depois do commit
    class_=AsyncSession,
    bind=engine,  # associa à engine criada, ou seja, todas as sessões vão usar a mesma conexão com o banco
)
