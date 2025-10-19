# registry -> registra tudo o que será uma tabela no banco
# criando registry único para garantir que todas as tabelas sejam criadas juntas (no mesmo banco)

from sqlalchemy.orm import registry

table_registry = registry()
