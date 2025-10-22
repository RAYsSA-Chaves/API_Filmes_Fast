# Lógica da API para requisições de gêneros

from http import HTTPStatus

from fastapi import APIRouter

from schemas.filme_schema import MessageSchema
from schemas.genero_schema import GeneroList, GeneroSchema

router = APIRouter(prefix='/generos', tags=['Gêneros'])


# Salvar um gênero novo
@router.post('/', status_code=HTTPStatus.CREATED, response_model=GeneroSchema)
def create_genero(genero: GeneroSchema):
    return genero


# Listar todos os gêneros
@router.get('/', status_code=HTTPStatus.OK, response_model=GeneroList)
def read_generos():
    return GeneroList


# Alterar um gênero
@router.put('/{genero_id}', status_code=HTTPStatus.OK, response_model=GeneroSchema)
def update_genero(genero_id: int, genero: GeneroSchema): 
    ...


# Deletar um gênero
@router.delete('/{genero_id}', status_code=HTTPStatus.OK, response_model=MessageSchema)
def delete_filme(genero_id: int): 
    ...
