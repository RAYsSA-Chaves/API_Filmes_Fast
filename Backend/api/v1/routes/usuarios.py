# Lógica da API para cadastro ou edição de usuários

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from core.security import get_password_hash
from models.user_model import UserModel
from schemas.user_schema import UserCreate, UserPublic

router = APIRouter(prefix='/usuarios', tags=['Usuários'])


# Cadastrar novo usuário
@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    # verificar se email já existe
    user_db = await db.scalar(select(UserModel).where(func.lower(UserModel.email) == user.email.lower()))
    if user_db:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Deu ruim! Email já cadastrado!')

    # cria usuário com hash de senha
    novo_usuario = UserModel(email=user.email, senha=get_password_hash(user.senha))

    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return novo_usuario


# Alterar dados de um cadastro
@router.put('/{user_id}', status_code=HTTPStatus.ACCEPTED, response_model=UserPublic)
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_session)):
    # verifica se usuário existe
    usuario = await db.get(UserModel, user_id)
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!')

    # verifica se o novo email não causa conflito
    email_duplicado = await db.scalar(
        select(UserModel).where(func.lower(UserModel.email) == user.email.lower() & UserModel.id != user_id)
    )
    if email_duplicado:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Email já cadastrado!')

    # atualiza os dados
    usuario.email = user.email
    usuario.senha = get_password_hash(user.senha)

    await db.commit()
    await db.refresh(usuario)
    return usuario


# Excluir um usuário
@router.delete('/{user_id}', status_code=HTTPStatus.OK)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    usuario = await db.get(UserModel, user_id)
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!')

    await db.delete(usuario)
    await db.commit()
    return {'message': f'Usuário {usuario.email} deletado com sucesso!'}
