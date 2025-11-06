# Hash de senhas e criação de token

from datetime import datetime, timezone, timedelta # timedelta -> armazena quantidades de tempo

from jwt import encode # gera o token e assinatura
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()  # ele decide sozinho como hashear

# Variáveis para o token
SECRET_KEY = 'my_super_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


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
