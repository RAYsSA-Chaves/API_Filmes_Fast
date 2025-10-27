# Lógica da API para requisições de filmes

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from models.filme_model import MovieModel
from models.genero_model import GeneroModel
from schemas.filme_schema import MessageSchema, MovieList, MoviePublic, MovieSchema

# Criando o roteador
router = APIRouter(prefix='/filmes', tags=['Filmes'])  # tags -> vai agrupar na documentação automática do FastAPI


# Salvar um novo filme
@router.post('/', status_code=HTTPStatus.CREATED, response_model=MoviePublic)
async def create_movie(filme: MovieSchema, db: AsyncSession = Depends(get_session)):
    # verificar se filme já existe
    filme_db = await db.scalar(
        select(MovieModel).where((MovieModel.titulo == filme.titulo) & (MovieModel.ano == filme.ano))
    )
    # retorna erro se já existir
    if filme_db:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Esse filme já existe!')

    # converte de objeto python para modelo do banco e salva
    novo_filme = MovieModel(
        titulo=filme.titulo,
        duracao=filme.duracao,
        ano=filme.ano,
        capa=filme.capa,
        avaliacao_interna=filme.avaliacao_interna,
        generos=[],
    )

    # pega os generos e verifica se existem
    for genero_id in filme.generos:
        genero = await db.get(GeneroModel, genero_id)
        if not genero:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Deu ruim! O gênero {genero_id} não existe no sistema!')
        novo_filme.generos.append(genero)

    await db.add(novo_filme)  # adiciona automaticamente na intermediária, porque filmes tem relationship com gêneros definida
    await db.commit()
    await db.refresh(novo_filme)  # atualiza com as coisas que estão no banco (pega id e created_at, que não passados pelo usuário)
    return novo_filme


# Listar todos os filmes
@router.get('/', status_code=HTTPStatus.OK, response_model=MovieList)
async def read_movies(
    page: int = Query(1, ge=1, description='Número da página'),
    per_page: int = Query(10, ge=1, description='Número de filmes por página'),
    db: AsyncSession = Depends(get_session),
):
    filmes = await db.scalars(
        select(MovieModel).limit(per_page).offset((page - 1) * per_page)
    )
    filmes = result.all()
    return {'filmes': filmes}

    # limit = retorna n registros no máximo
    # offset = pula os n primeiros registros; define a partir de qual ele começa a pegar
    # query = query string(valor padrão caso não seja passado nada, greater or equal to 1)


# Acessar um filme específico
@router.get('/{filme_id}', status_code=HTTPStatus.OK, response_model=MoviePublic)
async def read_one_movie(filme_id: int, db: AsyncSession = Depends(get_session)):
    # verificar se filme existe
    filme_db = await db.scalar(select(MovieModel).where(MovieModel.id == filme_id))
    if not filme_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim! Não achei o filme.')
    return filme_db


# Alterar um filme
@router.put('/{filme_id}', status_code=HTTPStatus.ACCEPTED, response_model=MoviePublic)
async def update_movie(filme_id: int, filme: MovieSchema, db: AsyncSession = Depends(get_session)):
    # verificar se filme existe
    filme_db = await db.scalar(select(MovieModel).where(MovieModel.id == filme_id))
    if not filme_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Filme não encontrado!')

    # verificar se o put vai gerar filme duplicado
    filme_duplicado = await db.scalar(
        select(MovieModel).where(
            (MovieModel.titulo == filme.titulo) & (MovieModel.ano == filme.ano) & (MovieModel.id != filme_id)
        )
    )
    if filme_duplicado:
        raise HTTPException(HTTPStatus.CONFLICT, detail='Esse filme já existe!')

    # verificar se foram enviados gêneros
    if not filme.generos or len(filme.generos) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='É obrigatório informar pelo menos um gênero para o filme!'
        )

    # alterar os dados
    filme_db.titulo = filme.titulo
    filme_db.duracao = filme.duracao
    filme_db.ano = filme.ano
    filme_db.capa = filme.capa
    filme_db.avaliacao_interna = filme.avaliacao_interna
    filme_db.generos = []

    # pega os generos e verifica se existem
    for genero_id in filme.generos:
        genero = await db.get(GeneroModel, genero_id)
        if not genero:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, 
                detail=f'Deu ruim! O gênero {genero_id} não existe no sistema!'
            )
    filme_db.generos = filme.generos

    # salva as alterações
    await db.commit()
    await db.refresh(filme_db)
    return filme_db


# Deletar um filme
@router.delete('/{filme_id}', status_code=HTTPStatus.OK, response_model=MessageSchema)
async def delete_filme(filme_id: int, db: AsyncSession = Depends(get_session)):
    # verificar se filme existe
    filme_db = await db.scalar(select(MovieModel).where(MovieModel.id == filme_id))
    if not filme_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim! Não achei o filme.')

    # deletar
    db.delete(filme_db)
    await db.commit()
    return {'message': f'Filme "{filme_db.titulo}" deletado com sucesso!'}
