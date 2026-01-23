# Hash de senhas e criação de token

from datetime import datetime, timedelta, timezone  # timedelta -> armazena quantidades de tempo

from jwt import (
    DecodeError,
    ExpiredSignatureError,
    decode,
    encode,
)  # encode -> transforma dados em token (formato seguro); decode -> converte de volta para os dados originais
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()  # ele decide sozinho como hashear


from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer  # extrai token Bearer do header HTTP
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from models import UserModel

# Variáveis para o token
SECRET_KEY = 'my_super_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/token')  # indica o endpoint onde o cliente pode obter o token

"""
    Uso do OAuth2PasswordBearer:
    - testar função de login;
    - digite usuário e senha e ele vai excutar a função de login e gerar o token
    - o token será passado nos headers das requisições automaticamente
"""


# Função para hashear uma senha
def get_password_hash(password: str):
    return pwd_context.hash(password)


# Função para validar uma senha passada com uma senha hasheada guardada no banco
def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# Função para criar token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Função para validar token (autorização)
async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    # padronizando erro:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Credenciais não puderam ser validadas',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        # tenta validar o token passado no header
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # pega info do usuário que era passada no token
        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    # trata erro de token expirado
    except ExpiredSignatureError:
        raise credentials_exception

    # busca se usuário existe no banco
    user = await db.scalar(select(UserModel).where(UserModel.email == subject_email))
    if not user:
        raise credentials_exception

    return user
