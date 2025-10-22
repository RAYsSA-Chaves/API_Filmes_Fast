# Lógica da API para requisições de filmes

from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from schemas.filme_schema import MessageSchema, MovieDB, MovieList, MoviePublic, MovieSchema

# Criando o roteador
router = APIRouter(prefix='/filmes', tags=['Filmes'])  # tags -> vai agrupar na documentação automática do FastAPI



# Salvar um novo filme no
@router.post('/', status_code=HTTPStatus.CREATED, response_model=MoviePublic)
def create_movie(filme: MovieSchema):
    
    return 


# Acessar um filme específico
@router.get('/{filme_id}', status_code=HTTPStatus.OK, response_model=MoviePublic)
def read_one_movie(filme_id: int):
    
    return


# Listar todos os filmes
@router.get('/', status_code=HTTPStatus.OK, response_model=MovieList)
def read_movies():
    return


# Alterar um filme
@router.put('/{fime_id}', status_code=HTTPStatus.OK, response_model=MoviePublic)
def update_movie(filme_id: int, filme: MovieSchema):
    return


# Deletar um filme
@router.delete('/{filme_id}', status_code=HTTPStatus.OK, response_model=MessageSchema)
def delete_filme(filme_id: int):
   return
