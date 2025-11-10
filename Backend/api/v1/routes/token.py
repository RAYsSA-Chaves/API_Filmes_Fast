# Lógica da API para validar credenciais e gerar token (Login)

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm  # formulário padrão da web de requisição de senha
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from core.security import create_access_token, verify_password
from models.user_model import UserModel
from schemas.token_schema import Token

# Criando o roteador
router = APIRouter(prefix='/token', tags=['Token'])


# Validar credenciais e gerar token (login)
@router.post(
    '/',
    response_model=Token,
    summary='Autenticação de Usuário',
    description=""" 
    Realiza login do usuário e gera token JWT.
    **Importante:** o campo `username` deve conter o `e-mail` do usuário!
    """,
)
async def login_for_access_token(
    formData: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)
):
    # verificar se usuário existe
    user_db = await db.scalar(select(UserModel).where(UserModel.email == formData.username))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Email e/ou senha incorreto(s)')

    # validar a senha passada
    if not verify_password(formData.password, user_db.senha):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Email e/ou senha incorreto(s)')

    # gerar token
    access_token = create_access_token({'sub': user_db.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
