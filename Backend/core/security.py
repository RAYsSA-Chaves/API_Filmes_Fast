# Hash de senhas e criação de token

from datetime import datetime, timezone, timedelta # timedelta -> armazena quantidades de tempo

from jwt import encode, decode, DecodeError  # encode -> transforma dados em token (formato seguro); decode -> converte de volta para os dados originais
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()  # ele decide sozinho como hashear

import secrets  # gera "segredos" / números aleatórios e secretos

from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer  # extrai token Bearer do header HTTP


# Variáveis para o token
SECRET_KEY = secrets.token.urlsafe(32)
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')  # indica o endpoint onde o cliente pode obter o token (documentação)


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
def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, SECRET_KEY, algorithm=ALGORITHM)
        subject_email = payload.get('sub')  # info do usuário que era passada no token
    except DecodeError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Esse filme já existe!')
