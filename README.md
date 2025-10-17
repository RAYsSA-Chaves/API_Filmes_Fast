# API de Filmes com FastAPI 
Aprendendo FastAPI.

O que é FastAPI?

FastAPI é um framework (como Flask ou Django) para construir APIs com Python, criado para ser rápido, simples e eficiente.

É chamado do Fast por ser realmente muito rápido. E sua velocidade vem do uso de código assíncrono de forma nativa, que permite requisições assíncronas (várias ao mesmo tempo sem travar o servidor).

------

O que é o Swagger?
O Swagger no FastAPI refere-se ao conjunto de ferramentas e à especificação OpenAPI que o FastAPI usa para gerar automaticamente documentação interativa de APIs. O FastAPI utiliza o Swagger UI para fornecer uma interface gráfica onde os desenvolvedores podem explorar, testar e interagir com a API diretamente do navegador, sem precisar escrever código HTML, CSS ou JavaScript para isso. 
Swagger e OpenAPI são ferramentas poderosas para criar APIs com FastAPI . Elas permitem gerar automaticamente a documentação da API, testar APIs usando uma interface web e validar solicitações e respostas para garantir que sua API esteja funcionando conforme o esperado. 
Acesso: caminho_da_sua_api/docs

-----

Framework:

Em português, framework significa estrutra de trabalho ou estrutura de suporte. É basicamente um conjunto de ferramentas, códigos, funções, organização de pastas e arquivos e regras prontas que ajudam a desenvolver programas rapidamente e de forma organizada.

Um framework oferece a base (esqueleto) para o seu projeto e você só precisa preencher com o seu código. 

-----

API:

Application Programming Interface ou Interface de Programação de Aplicativos é uma forma de dois sistemas diferentes trocarem informações entre si, geralmente em formato JSON.

Analogia: um garçom em um restaurante
Você (cliente) faz o pedido ao garçom 
O garçom (API) leva o seu pedido à cozinha (sistema que tem os dados)
A cozinha prepara a comida (processa o pedido)
O garçom retorna a comida para você (resposta da API)

Você nunca fala diretamente com a cozinha, sempre com o garçom. Da mesma forma, um aplicativo não acessa o banco de dados diretamente, ele fala com a API.

Uma API, então, é um conjunto de endpoints (endereços na web) que permitem pedir ou enviar dados.

Ex: uma API de filmes:

Você pode ter as ações:
Listar filmes - uma requisição do tipo GET - para o endpoint /filmes

Adicionar filme - uma requisição do tipo POST - para o endpoint /filmes

Exemplo: 
A API do Google Maps permite que outros aplicativos exibam mapas e rotas, sem precisar recriar todo o sistema do zero. 

Um streaming de filmes não necessariamente precisaria criar um banco e armazenar todas as infos de cada filme, como capa, sinopse, atores, etc, ele poderia consumir de uma API de filmes que já existe, que realizam requisições para um servidor de filmes que já existe.


API REST e RESTFUL (estilos) de API:
Rest (Respresentational State Transfer) é um padrão de boas práticas para APIs
- usa metodos HTTP (GET, POST, PULL, DELETE)
- os dados geralmente são enviados em formato json
- usa URLs para identificar recursos (/fimes, /usuarios)
- é stateless (o servidor não guarda informações da sessão do cliente e a API nem mesmo armazena o seu próprio estado)


Restful 
É uma API que segue corretamente os princípios REST, ou seja, toda API Restful é Rest.

- usa os metodos HTTP corretamente
- tem seus recursos (URLs) bem definidos
- é stateless 
- retorna respostas padronizadas, geralmente JSON com códigos HTTP corretos (200, 404...)
- usa HATEOAS (himermidia as the engine of application state) ou hipermidia como motor do estado da aplicação, em outras palavras, contém links dentro das respostas para outros recursos relacionados, tornando a API autoexplicativa, pois, assim, o cliente consegue navegar pela API dinamicamente sem precisar conhecer antecipadamente todas as URLs
Ex:
{
  "id": 1,
  "nome": "Rayssa",
  "curso": "DS",
  "_links": {
    "self": { "href": "/alunos/1" },
    "curso": { "href": "/cursos/ADS" },
    "todos_os_alunos": { "href": "/alunos" }
  }
}

A própria resposta ensina como continuar navegando, basta seguir os links sem precisar conhecer as rotas antes.


Exemplo de API nao Restful:
POST /api/getUsuarios

Aqui a ação está no nome da rota e não no método HTTP e isso viola o padrão Rest 


URL e URI:
URI - Uniform resource identifier - é um identificador genérico de recursos (qualquer coisa acessível na rede), ela serve para identificar um recurso, mas nao indica necessariamente como acessá-lo, onde está localizado
Ex: /usuarios/1

URL - uniform resource locator - é um tipo de URI que, além de identificar o recurso, informa onde ele está e como acessá-lo 

Toda URL é uma URI, mas nem toda URI é uma URL

Ex: https://api.meusite.com/usuarios/1


Endpoint:
URL + tipo de ação/interação com o recurso (método HTTP)

Principais ações possiveis
CRUD - create, read, updated e delete
Metodos HTTP que permitem realizar essas ações:
Post - criar novo item e cadastrar
Get - puxar e exibir
Put- atualizar dados
delete - deletar algo


------

Decoradores (@)
Os decoradores do FastAPI servem para definir rotas de API (como @app.get('/items') ou @app.post('/items')), associando uma função a um método HTTP e a um caminho específico. Eles também são usados para adicionar funcionalidades extras de forma elegante, como autenticação, validação de dados

Analogia do embrulho de presente:
Imagine que você tem um presente lindamente embrulhado. O presente dentro é o principal, certo? Mas o papel de embrulho, a fita e o laço o tornam especial, dão um toque especial e podem até revelar algo sobre o que está dentro ou como abri-lo.

Em Python, um decorador é como aquele embrulho de presente! É um tipo especial de função que literalmente "embrulha" outra função. Ao embrulhar essa função, ele pode:

Adicione um novo comportamento à função original sem alterar o código da própria função .
Modifique o funcionamento da função.
Forneça instruções adicionais sobre como a função deve ser usada.
Pense desta forma: você escreve uma função Python comum. Então, você adiciona um decorador a ela e pronto! Essa função original de repente ganha poderes ou instruções extras que não tinha antes.

@algo.get É um "Decorador de Operação de Caminho": O appobjeto (nosso aplicativo FastAPI) tem métodos como .get(), .post(), .put(), .delete(), etc. Esses métodos, quando usados ​​como decoradores, são incrivelmente poderosos.
Ele vincula um caminho de URL a uma função: o "/"interior @app.get("/")informa ao FastAPI: "Se alguém enviar uma solicitação HTTP GET para a URL raiz ( /), execute a função logo abaixo deste decorador ( read_rootneste caso)."
Ele adiciona superpoderes da Web: este decorador faz muito trabalho para você nos bastidores:
Ele informa ao aplicativo FastAPI para "escutar" solicitações naquele URL específico.
Ele lida automaticamente com a conversão do dicionário Python {"message": "Hello, World!"}em JSON (o formato de dados padrão para APIs da web) antes de enviá-lo de volta como uma resposta HTTP.
Ele sabe como gerar automaticamente aquela documentação interativa incrível (Swagger UI / ReDoc) para sua API!
Ele gerencia o envio do código de status HTTP correto (como 200 OK) junto com sua resposta.

Cada um deles adiciona comportamentos e instruções específicas relacionadas à web à função Python que eles decoram.

Passos para criar o projeto com fastapi:
Criação de env: python -m venv env
instalação do FastAPI: pip install "fastapi[standard]"
salvar dependências no arquivo requirements: pip freeze > requirements.txt 

Para rodar o projeto:
acessar pasta principal do projeto (FilmesAPI)
- criar env:
python -m venv env
ativar a env
cd env
cd Scripts
.\activate
sair da pasta da env e acessar a pasta principal novamente
instalar as dependencias contidas no requirements:
pip install -r requirements.txt

Requirements.txt é um arquivo de texto simples em Python que lista as bibliotecas e suas versões específicas que um projeto precisa para funcionar. Ele é usado para garantir que todos os colaboradores usem as mesmas dependências, facilitando a reprodutibilidade do ambiente de desenvolvimento. 

rodar o arquivo main.py (que contém a api): fastapi dev main.py
