# Lógica da API para validar credenciais e gerar token

from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm  # formulário padrão da web de requisição de senha
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session
from core.security import create_access_token, verify_password, create_refresh_token, verify_refresh_token
from models.user_model import UserModel
from schemas.token_schema import Token


router = APIRouter(prefix='/token', tags=['Token'])

Session = Annotated[AsyncSession, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


# Validar credenciais e gerar token (login)
@router.post(
    '/',
    response_model=Token,
    summary='Autenticação de Usuário',
    description='''
    Realiza login do usuário e gera token JWT.
    **Importante:** o campo `username` deve conter o `e-mail` do usuário!
    ''',
)
async def login_for_access_token(formData: OAuth2Form, db: Session):
    # verificar se usuário existe
    user_db = await db.scalar(
        select(UserModel)
        .where(UserModel.email == formData.username)
    )
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Email e/ou senha incorreto(s)')

    # validar a senha passada
    if not verify_password(formData.password, user_db.senha):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Email e/ou senha incorreto(s)')

    # gerar token
    access_token = create_access_token({'sub': user_db.email, 'type': 'access'})

    # gerar token de refresh
    refresh_token = create_refresh_token({'sub': user_db.email})

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }


# Refresh de token
@router.post(
    '/refresh',
    response_model=Token,
    summary='Refresh de Token',
)
async def refresh_access_token(refresh_token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Refresh token inválido'
    )

    payload = verify_refresh_token(refresh_token)

    if not payload:
        raise credentials_exception

    subject_email = payload.get('sub')
    if not subject_email: 
        raise credentials_exception

    user = await db.scalar(
        select(UserModel)
        .where(UserModel.email == subject_email)
    )

    if not user:
        raise credentials_exception

    new_access_token = create_access_token({
        'sub': user.email,
        'type': 'access'
    })

    new_refresh_token = create_refresh_token({
        'sub': user.email
    })

    return {
        'access_token': new_access_token,
        'refresh_token': new_refresh_token,
        'token_type': 'bearer'
    }