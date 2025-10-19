# Lógica da API para requisições de gêneros + filmes

from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from schemas.filme_schema import MessageSchema
from schemas.genero_filme_schema import GeneroFilmeList, GeneroFilmeSchema

router = APIRouter(prefix='/generos-filmes', tags=['Associações'])

fake_db = []


# Salvar uma nova associação de gênero e filme
@router.post('/', status_code=HTTPStatus.CREATED, response_model=GeneroFilmeSchema)
def associar_genero_filme(item: GeneroFilmeSchema):
    fake_db.append(item)
    return item


# Listar todas as associações
@router.get('/', response_model=GeneroFilmeList)
def read_associacoes():
    return GeneroFilmeList(generos_filmes=fake_db)


# Listar filmes de um gênero
@router.get('/genero/{id_genero}', response_model=GeneroFilmeList)
def read_filmes_do_genero(id_genero: int):
    resultado = []
    for associacao in fake_db:
        if associacao['id_genero'] == id_genero:
            resultado.append(associacao)

    if not resultado:
        raise HTTPException(status_code=404, detail='Nenhum filme encontrado para este gênero!')

    return GeneroFilmeList(generos_filmes=resultado)


# Listar gêneros de um filme
@router.get('/filme/{id_filme}', response_model=GeneroFilmeList)
def read_generos_do_filme(id_filme: int):
    resultado = []
    for associacao in fake_db:
        if associacao['id_filme'] == id_filme:
            resultado.append(associacao)

    if not resultado:
        raise HTTPException(status_code=404, detail='Este filme não possui gênero!')

    return GeneroFilmeList(generos_filmes=resultado)


# Deletar uma associação
@router.delete('/{id_genero}/{id_filme}', status_code=HTTPStatus.OK, response_model=MessageSchema)
def delete_associacao(id_genero: int, id_filme: int):
    for associacao in fake_db:
        if associacao['id_genero'] == id_genero and associacao['id_filme'] == id_filme:
            del fake_db[associacao]
            return {'message': 'Associação filme_genero deletada com sucesso.'}

    raise HTTPException(status_code=404, detail='Deu ruim! Associação não encontrada.')
