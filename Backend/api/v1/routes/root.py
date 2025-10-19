# Retorno da "home" ou raiz (teste)

from http import HTTPStatus

from fastapi import APIRouter

from schemas.filme_schema import MessageSchema

# Criando o roteador
router = APIRouter()


@router.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def read_root():
    return {'message': 'Olá mundo! Estou funcionando!'}
