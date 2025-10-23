# registry -> registra tudo o que será uma tabela no banco
# criando registry único para garantir que todas as tabelas sejam criadas juntas (no mesmo banco)

from sqlalchemy.orm import registry

table_registry = registry()

# importando os models para o python executar o decorator desses arquivos e registrar as tabelas no metadata
from .filme_model import MovieModel as MovieModel
from .genero_filme_model import GeneroFilmeModel as GeneroFilmeModel
from .genero_model import GeneroModel as GeneroModel
