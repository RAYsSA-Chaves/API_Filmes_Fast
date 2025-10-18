# Lógica principal da API

from http import HTTPStatus

from fastapi import FastAPI

from schemas import MessageSchema

app = FastAPI(title="Minha API de Filmes")


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)  # retorno da "home" ou raiz
# Função de teste
def read_root():
    return {'message': 'Olá mundo! Estou funcionando!'}
