# Lógica da API para requisições de filmes usando fake db

# from http import HTTPStatus

# from fastapi import APIRouter, HTTPException

# from schemas.filme_schema import MessageSchema, MovieDB, MovieList, MoviePublic, MovieSchema

# # Criando o roteador
# router = APIRouter(prefix='/filmes', tags=['Filmes'])  # tags -> vai agrupar na documentação automática do FastAPI

# fake_db = []


# # Salvar um novo filme no
# @router.post('/', status_code=HTTPStatus.CREATED, response_model=MoviePublic)
# def create_movie(filme: MovieSchema):
#     filme_with_id = MovieDB(
#         titulo=filme.titulo,
#         duracao=filme.duracao,
#         ano=filme.ano,
#         capa=filme.capa,
#         avaliacao_interna=filme.avaliacao_interna,
#         id=len(fake_db) + 1,  # cria id automaticamente
#     )
#     fake_db.append(filme_with_id)  # guarda no banco falso
#     return filme_with_id


# # Acessar um filme específico
# @router.get('/{filme_id}', status_code=HTTPStatus.OK, response_model=MoviePublic)
# def read_one_movie(filme_id: int):
#     # se o filme passado não existir
#     if filme_id < 1 or filme_id > len(fake_db):
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim! Não achei o filme.')

#     return fake_db[filme_id - 1]


# # Listar todos os filmes
# @router.get('/', status_code=HTTPStatus.OK, response_model=MovieList)
# def read_movies():
#     return {'filmes': fake_db}


# # Alterar um filme
# @router.put('/{fime_id}', status_code=HTTPStatus.OK, response_model=MoviePublic)
# def update_movie(filme_id: int, filme: MovieSchema):
#     filme_with_id = MovieDB(**filme.model_dump(), id=filme_id)  # pega todos os campos do filme e acrescenta id

#     # se o filme passado não existir
#     if filme_id < 1 or filme_id > len(fake_db):
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim! Não achei o filme.')

#     fake_db[filme_id - 1] = filme_with_id  # pega o filme no banco e modifica

#     return filme_with_id


# # Deletar um filme
# @router.delete('/{filme_id}', status_code=HTTPStatus.OK, response_model=MessageSchema)
# def delete_filme(filme_id: int):
#     # se o filme passado não existir
#     if filme_id < 1 or filme_id > len(fake_db):
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim! Não achei o filme.')

#     filme_nome = fake_db[filme_id - 1].titulo
#     del fake_db[filme_id - 1]
#     return {'message': f'Filme "{filme_nome}" deletado.'}
