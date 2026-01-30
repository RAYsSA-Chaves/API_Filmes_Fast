# Lógica da API para requisições de filmes

from http import HTTPStatus
from typing import (
    Annotated,
)  # permite criar uma anotação para deixar definido um tipo reutilizável e os seus metadados (infos dele); não executa código, apenas fornece uma info sobre o tipo, por exemplo: de onde obter o seu valor

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.deps import get_session
from core.security import (
    get_current_user,
)  # vai impedir usuários não logados de acessar os endpoints (uso como dependência) -> coloca cadeado lá no Swagger
from models.filme_model import MovieModel
from models.genero_model import GeneroModel
from models.user_model import UserModel
from schemas.filme_schema import MessageSchema, MovieList, MoviePublic, MovieSchema, FilterMovie, MovieUpdate

# Criando o roteador
router = APIRouter(prefix='/filmes', tags=['Filmes'])  # tags -> vai agrupar na documentação automática do FastAPI

Session = Annotated[
    AsyncSession, Depends(get_session)
]  # traduzindo: a variável Session é uma AsyncSession que o FastAPI deve obter usando get_session

CurrentUser = Annotated[UserModel, Depends(get_current_user)]


# Salvar um novo filme
@router.post('/', status_code=HTTPStatus.CREATED, response_model=MoviePublic)
async def create_movie(filme: MovieSchema, db: Session, current_user: CurrentUser):
    # verificar se filme já existe
    filme_db = await db.scalar(
        select(MovieModel).where(
            (func.lower(MovieModel.titulo) == (filme.titulo.lower())) & (MovieModel.ano == filme.ano)
        )
    )
    # retorna erro se já existir
    if filme_db:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Esse filme já existe!')

    # verificar se capa já foi usada
    filme_capa = await db.scalar(select(MovieModel).where((MovieModel.capa == filme.capa)))
    # retorna erro se já existir
    if filme_capa:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Essa capa já foi usada para outro filme!')

    # pega os generos e verifica se existem
    generos_db = []
    for genero_id in filme.generos:
        genero = await db.get(GeneroModel, genero_id)
        if not genero:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f'Deu ruim! O gênero {genero_id} não existe no sistema!'
            )
        generos_db.append(genero)

    # converte de objeto python para modelo do banco e salva
    novo_filme = MovieModel(
        titulo=filme.titulo,
        duracao=filme.duracao,
        ano=filme.ano,
        capa=str(filme.capa),
        avaliacao_interna=filme.avaliacao_interna,
        classificacao=filme.classificacao,
        generos=generos_db,  # adiciona automaticamente na intermediária, porque filmes tem relationship com gêneros definida
        created_by=current_user.id,
    )

    db.add(novo_filme)
    await db.commit()
    await db.refresh(
        novo_filme, attribute_names=['generos']
    )  # atualiza com as coisas que estão no banco (pega id e created_at, que não passados pelo usuário)

    return novo_filme


# Listar todos os filmes
@router.get('/', status_code=HTTPStatus.OK, response_model=MovieList)
async def read_movies(
    db: Session,
    filmes_filter: Annotated[FilterMovie, Query()],
):
    
    # filtrando
    query = select(MovieModel)
    
    if filmes_filter.titulo:
        query = query.filter(MovieModel.titulo.contains(filmes_filter.titulo))

    if filmes_filter.ano:
        query = query.filter(MovieModel.ano == filmes_filter.ano)

    if filmes_filter.genero:
        query = query.join(MovieModel.generos).where(
            GeneroModel.id.in_(filmes_filter.genero)
        )

    # explicando o filtro dos gêneros
    # filme já foi acessado, agora preciso dos dados relacionados -> ORM resolve sozinho com selectionload
    # quais filmes devo trazer (depende de filtros)? -> ORM não resolve sozinho porque ele ainda não tem o filme, precisa de JOIN explícito

    filmes = await db.scalars(
        query
        .options(
            selectinload(MovieModel.generos), selectinload(MovieModel.usuario)
        )  # força carregar os gêneros e usuarios
        .limit(filmes_filter.limit)
        .offset((filmes_filter.page - 1) * filmes_filter.limit)
    )
    return {'filmes': filmes.all()}

    # limit = retorna n registros no máximo
    # offset = pula os n primeiros registros; define a partir de qual ele começa a pegar
    # Query = indica que vai vir via parâmetros na url


# Acessar um filme específico
@router.get('/{filme_id}', status_code=HTTPStatus.OK, response_model=MoviePublic)
async def read_one_movie(filme_id: int, db: Session):
    # verificar se filme existe
    filme_db = await db.scalar(
        select(MovieModel)
        .where(MovieModel.id == filme_id)
        .options(
            selectinload(MovieModel.generos),
            selectinload(MovieModel.usuario)
        )
    )
    if not filme_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim! Não achei o filme.')
    return filme_db


# Listar filmes cadastrados por um usuário
@router.get('/usuario/{user_id}', status_code=HTTPStatus.OK, response_model=MovieList)
async def read_user_movies(user_id: int, db: Session):
    # verificar se existem filmes cadastrados pelo usuário
    filmes_db = await db.scalars(
        select(MovieModel)
        .where(MovieModel.created_by == user_id)
        .options(
            selectinload(MovieModel.generos),
        )
    )

    lista = filmes_db.all(),

    if not lista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Não encontrei filmes cadastrados por esse usuário.'
        )
    
    return {'filmes': lista}


# Alterar um filme
@router.put('/{filme_id}', status_code=HTTPStatus.ACCEPTED, response_model=MoviePublic)
async def update_movie(filme_id: int, filme: MovieSchema, db: Session, current_user: CurrentUser):
    # verificar se filme existe
    filme_db = await db.scalar(
        select(MovieModel).where(MovieModel.id == filme_id).options(selectinload(MovieModel.generos))
    )
    if not filme_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Filme não encontrado!')

    # verificar se o put vai gerar filme duplicado
    filme_duplicado = await db.scalar(
        select(MovieModel).where(
            (func.lower(MovieModel.titulo) == (filme.titulo.lower()))
            & (MovieModel.ano == filme.ano)
            & (MovieModel.id != filme_id)
        )
    )
    if filme_duplicado:
        raise HTTPException(HTTPStatus.CONFLICT, detail='Esse filme já existe!')

    # verificar capa duplicada
    capa_duplicada = await db.scalar(
        select(MovieModel).where((MovieModel.capa == filme.capa) & (MovieModel.id != filme_id))
    )
    if capa_duplicada:
        raise HTTPException(HTTPStatus.CONFLICT, detail='Essa capa já foi usada para outro filme!')

    # verificar se foram enviados gêneros
    if not filme.generos or len(filme.generos) == 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='É obrigatório informar pelo menos um gênero para o filme!'
        )

    # alterar os dados
    filme_db.titulo = filme.titulo
    filme_db.duracao = filme.duracao
    filme_db.ano = filme.ano
    filme_db.capa = str(filme.capa)
    filme_db.avaliacao_interna = filme.avaliacao_interna
    filme_db.classificacao = filme.classificacao
    filme_db.generos = []

    # pega os generos e verifica se existem
    for genero_id in filme.generos:
        genero = await db.get(GeneroModel, genero_id)
        if not genero:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f'Deu ruim! O gênero {genero_id} não existe no sistema!'
            )
        filme_db.generos.append(genero)

    # salva as alterações
    await db.commit()
    await db.refresh(filme_db)
    return filme_db


# Alterar filme sem precisar passar todos os dados
@router.patch('/{filme_id}', status_code=HTTPStatus.ACCEPTED, response_model=MoviePublic)
async def patch_movie(filme_id: int, filme: MovieUpdate, db: Session, current_user: CurrentUser):
    # verificar se filme existe
    filme_db = await db.scalar(
        select(MovieModel).where(MovieModel.id == filme_id).options(selectinload(MovieModel.generos))
    )
    if not filme_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Filme não encontrado!')

    # verificar se vai gerar filme duplicado
    if filme.titulo is not None or filme.ano is not None:
        filme_duplicado = await db.scalar(
            select(MovieModel).where(
                (func.lower(MovieModel.titulo) == (filme.titulo.lower()))
                & (MovieModel.ano == filme.ano)
                & (MovieModel.id != filme_id)
            )
        )
        if filme_duplicado:
            raise HTTPException(HTTPStatus.CONFLICT, detail='Esse filme já existe!')

    # verificar capa duplicada
    if filme.capa is not None:
        capa_duplicada = await db.scalar(
            select(MovieModel).where((MovieModel.capa == filme.capa) & (MovieModel.id != filme_id))
        )
        if capa_duplicada:
            raise HTTPException(HTTPStatus.CONFLICT, detail='Essa capa já foi usada para outro filme!')

    # pega os generos e verifica se existem
    if filme.generos is not None:
        if len(filme.generos) == 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='A lista de gêneros não pode ser vazia.'
            )
        
        filme_db.generos = []
    
        for genero_id in filme.generos:
            genero = await db.get(GeneroModel, genero_id)
            if not genero:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail=f'Deu ruim! O gênero {genero_id} não existe no sistema!'
                )
            filme_db.generos.append(genero)

    # excluir todos os campos que não foram passados e atualizar o que foi
    for key, value in filme.model_dump(exclude_unset=True).items():
        setattr(filme_db, key, value)

    # salva as alterações
    await db.commit()
    await db.refresh(filme_db)
    return filme_db


# Deletar um filme
@router.delete('/{filme_id}', status_code=HTTPStatus.OK, response_model=MessageSchema)
async def delete_filme(filme_id: int, db: Session, current_user: CurrentUser):
    # verificar se filme existe
    filme_db = await db.scalar(select(MovieModel).where(MovieModel.id == filme_id))
    if not filme_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim! Não achei o filme.')

    # deletar
    await db.delete(filme_db)
    await db.commit()
    return {'message': f'Filme {filme_db.titulo} deletado com sucesso!'}
