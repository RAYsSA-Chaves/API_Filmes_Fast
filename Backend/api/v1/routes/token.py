# Lógica da API para testar validação de credenciais

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import OAuth2PasswordRequestForm # formulário padrão da web de requisição de senha
from core.security import get_password_hash, verify_password

from core.deps import get_session
from models.user_model import UserModel
from schemas.user_schema import UserPublic


# Criando o roteador
router = APIRouter(prefix='/token', tags=['Token'])


# Validar credenciais
@router.post('/')
async def login_for_access_token(formData: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    # verificar se usuário existe
    user_db = await db.scalar(select(UserModel).where(UserModel.email == formData.email))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Email e/ou senha incorreto(s)')
    
    # validar a senha passada
    if not verify_password(formData.senha, user_db.senha):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Email e/ou senha incorreto(s)')
