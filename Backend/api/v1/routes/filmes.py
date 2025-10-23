# Lógica da API para requisições de filmes

from http import HTTPStatus

from fastapi import APIRoute, Depends, Response, HTTPException

from schemas.filme_schema import MessageSchema, MovieList, MoviePublic, MovieSchema
from models.filme_model import MovieModel
from models.genero_model import GeneroModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.deps import get_session

# Criando o roteador
router = APIRouter(prefix='/filmes', tags=['Filmes'])  # tags -> vai agrupar na documentação automática do FastAPI


# Salvar um novo filme no
@router.post('/', status_code=HTTPStatus.CREATED, response_model=MoviePublic)
def create_movie(filme: MovieSchema, db: AsyncSession = Depends(get_session)):
    # verificar se filme já existe
    filme_db = db.scalar(
        select(MovieModel).where(
            (MovieModel.titulo == filme.titulo) & (MovieModel.ano == filme.ano)
        )
    )
    # retorna erro se já existir
    if filme_db:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Esse filme já existe!')

    # adiciona no banco
    filme_db = MovieModel(
        titulo = filme.titulo,
        duracao = filme.duracao,
        ano = filme.ano,
        capa = filme.capa,
        avaliacao_interna = filme.avaliacao_interna
    )

    # pega os generos
    for genero_id in filme.generos:
        genero = db.get(GeneroModel, genero_id)
        filme_db.generos.append(genero)

    db.add(filme_db)
    db.commit()
    db.refresh(filme_db) # atualiza com as coisas que estão no banco (id e created_at, que não passados pelo usuário)
    return filme_db


# Acessar um filme específico
@router.get('/{filme_id}', status_code=HTTPStatus.OK, response_model=MoviePublic)
def read_one_movie(filme_id: int):
    return


# Listar todos os filmes
@router.get('/', status_code=HTTPStatus.OK, response_model=MovieList)
def read_movies():
    return


# Alterar um filme
@router.put('/{fime_id}', status_code=HTTPStatus.OK, response_model=MoviePublic)
def update_movie(filme_id: int, filme: MovieSchema):
    return


# Deletar um filme
@router.delete('/{filme_id}', status_code=HTTPStatus.OK, response_model=MessageSchema)
def delete_filme(filme_id: int):
    return
