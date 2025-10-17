from fastapi import FastAPI

app = FastAPI()


@app.get('/')  # retorno da "home" ou raiz
# Função de teste
def read_root():
    return {'message': 'Olá mundo! Estou funcionando!'}
