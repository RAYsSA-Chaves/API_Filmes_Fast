# Lógica da API para cadastro ou edição de usuários

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from core.security import get_current_user, get_password_hash
from models.user_model import UserModel
from schemas.filme_schema import MessageSchema
from schemas.user_schema import UserCreate, UserPublic, UserUpdate

router = APIRouter(prefix='/usuarios', tags=['Usuários'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[UserModel, Depends(get_current_user)]


# Cadastrar novo usuário
@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserCreate, db: Session):
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


# Acessar suas próprias infos
@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def read_logged_user(
    user_id: int,
    db: Session,
    current_user: CurrentUser,
):
    # verificar se usuário existe
    user_db = await db.scalar(select(UserModel).where(UserModel.id == user_id))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado :(')

    # verificar se quer acessar as infos de outros usuários
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Permissões insuficientes!')

    return user_db


# Alterar dados de um cadastro
@router.put('/{user_id}', status_code=HTTPStatus.ACCEPTED, response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserCreate,
    db: Session,
    current_user: CurrentUser,  # verifica se usuário existe
):
    # apenas o usuario pode alterar seu próprio cadastro
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Permissões insuficientes!')

    # verifica se o novo email não causa conflito
    email_duplicado = await db.scalar(
        select(UserModel).where((func.lower(UserModel.email) == user.email.lower()) & (UserModel.id != user_id))
    )
    if email_duplicado:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Email já cadastrado!')

    # atualiza os dados
    current_user.email = user.email
    current_user.senha = get_password_hash(user.senha)

    await db.commit()
    await db.refresh(current_user)
    return current_user


# Alterar cadastro sem precisar alterar todos os dados
@router.patch('/{user_id}', status_code=HTTPStatus.ACCEPTED, response_model=UserPublic)
async def patch_user(
    user_id: int,
    user: UserUpdate,
    db: Session,
    current_user: CurrentUser,
):
     # apenas o usuario pode alterar seu próprio cadastro
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Permissões insuficientes!')
    
    # verifica se o novo email não causa conflito
    if user.email:
        email_duplicado = await db.scalar(
        select(UserModel)
        .where((func.lower(UserModel.email) == user.email.lower()) & (UserModel.id != user_id))
    )
    if email_duplicado:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Email já cadastrado!')
    
    # excluir todos os campos que não foram passados e atualizar o que foi
    for key, value in user.model_dump(exclude_unset=True).items():
        if user.senha:
            user.senha = get_password_hash(user.senha)
        setattr(current_user, key, value)

    await db.commit()
    await db.refresh(current_user)
    return current_user



# Excluir um usuário
@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=MessageSchema)
async def delete_user(user_id: int, db: Session, current_user: CurrentUser):
    # apenas o próprio usuário pode deletar a sua conta
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Permissões insuficientes!')

    await db.delete(current_user)
    await db.commit()
    return {'message': f'Usuário {current_user.email} deletado com sucesso!'}
