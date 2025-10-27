# Lógica da API para requisições de gêneros

from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session

from schemas.filme_schema import MessageSchema
from schemas.genero_schema import GeneroList, GeneroSchema

from models.filme_model import MovieModel
from models.genero_model import GeneroModel

router = APIRouter(prefix='/generos', tags=['Gêneros'])


# Salvar um gênero novo
@router.post('/', status_code=HTTPStatus.CREATED, response_model=GeneroSchema)
async def create_genero(genero: GeneroSchema, db: AsyncSession = Depends(get_session)):
    # verificar se o gênero já existe
    genero_db = await db.scalar(select(GeneroModel).where(GeneroModel.genero == genero.genero))
    # retorna erro se já existir
    if genero_db:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=f'Esse gênero já existe!')

    # converte de objeto python para modelo do banco e salva
    novo_genero = GeneroModel(genero=genero.genero)
    db.add(novo_genero)
    await db.commit()
    await db.refresh(novo_genero)
    return novo_genero


# Listar todos os gêneros
@router.get('/', status_code=HTTPStatus.OK, response_model=GeneroList)
async def read_generos(
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(10, ge=1, description="Número de gêneros por página"),
    db: AsyncSession = Depends(get_session),
):
    generos = await db.scalars(
        select(GeneroModel).limit(per_page).offset((page - 1) * per_page)
    )
    generos = result.all()
    return {'generos': generos}


# Alterar um gênero
@router.put('/{genero_id}', status_code=HTTPStatus.OK, response_model=GeneroSchema)
async def update_genero(genero_id: int, genero: GeneroSchema, db: AsyncSession = Depends(get_session)):
    # verificar se o gênero existe
    genero_db = await db.scalar(select(GeneroModel).where(GeneroModel.id == genero_id))
    if not genero_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Gênero não encontrado!")

    # verificar se o put vai gerar gênero duplicado
    genero_duplicado = await db.scalar(
        select(GeneroModel).where(
            (GeneroModel.genero == genero.genero) & (GeneroModel.id != genero_id)
        )
    )
    if genero_duplicado:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=f'Esse gênero já existe!')

    # alterar o nome e salvar as alterações
    genero_db.genero = genero.genero
    await db.commit()
    await db.refresh(genero_db)
    return genero_db


# Deletar um gênero
@router.delete('/{genero_id}', status_code=HTTPStatus.OK, response_model=MessageSchema)
async def delete_genero(genero_id: int, db: AsyncSession = Depends(get_session)):
    # verificar se o gênero existe
    genero_db = await db.scalar(select(GeneroModel).where(GeneroModel.id == genero_id))
    if not genero_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Deu ruim! Não achei o gênero.")

    # deletar
    await db.delete(genero_db)
    await db.commit()
    return {'message': f'Gênero "{genero_db.genero}" deletado com sucesso!'}