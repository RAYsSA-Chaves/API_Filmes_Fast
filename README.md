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

URL - uniform resource locator - é um tipo de URI que, além de identificar o recurso, informa onde ele está e como acessá-lo através do protocolo http

Toda URL é uma URI, mas nem toda URI é uma URL

Protocolo HTTP (HyperText Transfer Protocol (Protocolo de Transferência de Hipertexto)) - É o protocolo de comunicação usado na web — ele define como o navegador (cliente) e o servidor trocam informações, como páginas, imagens, vídeos, APIs etc.
O HTTP segue o modelo cliente-servidor:
Cliente (ex: seu navegador ou aplicativo) → faz um pedido (requisição).
Servidor (ex: o site que você acessa) → envia uma resposta.
🔁 Esse ciclo se chama requisição e resposta HTTP.

Quando voce acessa: https://www.google.com
O navegador envia uma requisição HTTP para o servidor da Google, pedindo a página principal.
O servidor responde com um documento HTML, que o navegador renderiza na tela.
🧱 Estrutura de uma Requisição HTTP
Uma requisição é composta por:
Método → diz o que você quer fazer (GET, POST, etc)
URL (Uniform Resource Locator) → indica o recurso: GET /usuarios HTTP/1.1
Cabeçalhos (Headers) → informações adicionais:
Host: www.site.com
Content-Type: application/json
Authorization: Bearer xxxxxx
Corpo (Body) → conteúdo enviado (usado em POST, PUT etc):
{
  "nome": "Rayssa",
  "idade": 25
}

Resposta do servidor:
Código de status (Status Code)
Indica se deu certo ou não: 200, 402, 201, 400, etc
Cabeçalhos (Headers)
Informações sobre a resposta, ex:
Content-Type: text/html
Cache-Control: no-cache
Corpo (Body)
O conteúdo da resposta (HTML, JSON, imagem, etc).
Ou (em casos de requisições do tipo POST, PUT...): retorna o resultado da requisição no corpo:
{
  "id": 123,
  "nome": "Rayssa",
  "idade": 25,
  "mensagem": "Usuário criado com sucesso!"
}

{
  "erro": "Campo 'nome' é obrigatório"
}

http ou https - o 's' acrescenta uma camada de segurança, pois ele cripta a mensagem (ninguém pode interceptar senhas, pro exemplo)

Composição de uma URL:
Ex: http://api.meusite.com/usuarios/1:8000?query#fragmento
http:// = protocolo HTTP
api.meusite.com = endereço
/usuarios/1 = caminho do recurso (URI)
:8000 = porta (geralmente por padrão do protocolo HTTP)
?qurey = parametros de filtragem, ex: ?nome=Rayssa&idade=25
Conjunto de pares chave=valor usados para filtrar, pesquisar ou enviar dados leves na URL.
outro exemplo:
https://api.meusite.com/produtos?categoria=livros&precoMax=50
Isso significa:
O cliente quer produtos
Onde a categoria é livros
E o preço máximo é 50

#fragmento = Parte usada somente pelo navegador, não vai para o servidor. Serve para indicar uma seção específica dentro da página, como uma âncora interna na página (ex: ir direto para um trecho do texto).
ex: https://meusite.com/artigo#comentarios
➡ O navegador vai abrir a página artigo, e rolar automaticamente até o elemento com o identificador id="comentarios" no HTML.

Endpoint:
URL + tipo de ação/interação com o recurso (método HTTP)

Principais ações possiveis
CRUD - create, read, updated e delete
Metodos HTTP que permitem realizar essas ações:
Post - criar novo item e cadastrar
Get - puxar e exibir
Put- atualizar um recurso existente
delete - deletar um recurso


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

Exemplo de funcionamento de requisição com múltiplos parâmetros:
Cliente: http://localhost:8000/produtos?categoria=livros&preco_min=20&preco_max=50

Código em FastAPI (servidor):
@app.get("/produtos")
def listar_produtos(categoria: str = None, preco_min: float = None, preco_max: float = None):
    return {
        "categoria": categoria,
        "preco_mínimo": preco_min,
        "preco_máximo": preco_max,
        "mensagem": "Parâmetros recebidos com sucesso!"
    }

Os parâmetros categoria, preco_min e preco_max são opcionais (= None).
Quando você acessa a URL com ?categoria=livros&preco_min=20&preco_max=50,
o FastAPI automaticamente:
lê cada valor da query string;
converte o tipo (ex: float, str);
e entrega para a função listar_produtos.
Resposta do server:
O corpo da requisição (body) fica vazio, pois o método é GET.
A função retorna um JSON como resposta:
{
  "categoria": "livros",
  "preco_mínimo": 20.0,
  "preco_máximo": 50.0,
  "mensagem": "Parâmetros recebidos com sucesso!"
}


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
o que este comando faz: ele cria um server com recarregamento automático na nossa própria máquina (devido ao modo de desenvolvimento que passamos) para servir o arquvo main.py, então nós, como clientes, podemos requisitar e acessar as rotas desse arquivo no browser.
Por trás dos panos, o fastapi inicia o Uvicorn com --reload ativado (ele é o verdadeiro servidor da aplicação e permite receber as requisições HTTP do navegador, entregar essas requisições para o FastAPI, enviar as respostas de volta para o usuário.)

| Uvicorn                                       | FastAPI                                                 |
| --------------------------------------------- | ------------------------------------------------------- |
| É o **servidor** que executa a aplicação      | É o **framework** que define as rotas e regras          |
| Lida com as **requisições HTTP**              | Lida com a **lógica do sistema**                        |
| Pode rodar qualquer app ASGI (não só FastAPI) | Precisa de um servidor ASGI (como Uvicorn ou Hypercorn) |

Podemos abrir o servidor do uvicorn para rede local, assim, toda a sua rede (todos os dispositivos conectados na rede) conseguirão acessar através do seu próprio ip.

fastapi dev main.py --host 0.0.0.0

Acessando: descubra o ip do dispositivo que está servindo a API (ipconfig no windows)
Acesse o endereço na porta 8000 em qualquer disposivo conectado na rede, ex: 192.168.1.3:8000



# Acesso ao Backend via FrontEnd
Quando você acessa pelo frontend (um site, por exemplo), o servidor web ou o JavaScript do navegador pega esses dados da API e monta o HTML da página dinamicamente.

Existem dois jeitos principais disso acontecer:
1. Renderização no servidor (Server-Side Rendering – SSR)
O servidor (por exemplo, em FastAPI, Flask, ou Django) faz tudo antes de mandar o HTML já pronto pro navegador:
O servidor busca os dados internamente (não é necessário construir a API).
O servidor gera o HTML já pronto com os dados inseridos.
O navegador exibe o HTML completo.

2. Renderização no cliente (Client-Side Rendering – CSR)
Aqui, quem chama a API (em FasAPI, Django, etc) é o frontend, via JavaScript (normalmente usando fetch, axios, etc).
O navegador acessa o site, que carrega o HTML e o JavaScript.
O JavaScript faz uma requisição à API (GET, POST etc).
Quando o JSON chega, o JS atualiza o HTML dinamicamente.
O HTML é carregado primeiro.
O JavaScript chama a API e preenche o conteúdo depois.
É o que frameworks modernos como React, Vue e Angular fazem automaticamente.

⚖️ Comparando os dois jeitos
| Característica        | Server-Side Rendering (SSR) | Client-Side Rendering (CSR)             |
| :-------------------- | :-------------------------- | :-------------------------------------- |
| Onde o HTML é montado | No servidor                 | No navegador                            |
| Velocidade inicial    | Mais rápida (já vem pronta) | Mais lenta (espera o JS carregar)       |
| Atualização de dados  | Recarrega a página          | Atualiza via JavaScript                 |
| Ideal para            | Sites estáticos, SEO        | Aplicações dinâmicas (SPAs, dashboards) |


|                              | SSR – *Server-Side Rendering*                 | CSR – *Client-Side Rendering*                                        |
| :--------------------------- | :-------------------------------------------- | :------------------------------------------------------------------- |
| **Onde o HTML é montado**    | No **servidor** antes de enviar ao navegador  | No **navegador**, depois que o JavaScript roda                       |
| **O que o navegador recebe** | HTML **completo e pronto para exibir**        | Um HTML “vazio” + **JavaScript** que vai buscar os dados e preencher |
| **Como os dados chegam**     | O servidor busca no banco e já insere no HTML | O navegador faz requisições à API para pegar os dados                |


Se o usuário só vai ler conteúdo, prefira SSR.
Se o usuário vai interagir bastante, use CSR.

| Modelo  | Quem gera o HTML | Backend devolve | Pode usar qualquer framework? |
| ------- | ---------------- | --------------- | ----------------------------- |
| **SSR** | O servidor       | HTML pronto     | ✅ Sim                         |
| **CSR** | O navegador      | JSON (API)      | ✅ Sim                         |

🧱 Como funciona no SSR
Você cria templates HTML (com Django, Flask, FastAPI + Jinja2, etc.)
Pode adicionar CSS para o estilo e JavaScript para interatividade mínima
O servidor pega os dados (do banco, de uma API interna, etc.) e preenche os templates
O navegador recebe HTML já pronto, pronto para exibir

🔹 Estrutura típica SSR
projeto/
│
├─ templates/        # HTML do frontend (templates)
│   └─ produtos.html
├─ static/           # CSS, JS, imagens
│   ├─ style.css
│   └─ main.js
├─ app.py            # Servidor (FastAPI, Flask)
└─ banco.db          # Banco de dados

No servidor você faria algo assim (FastAPI + Jinja2):
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/produtos")
def pagina_produtos(request: Request):
    produtos = [
        {"nome": "Livro A", "preco": 30},
        {"nome": "Livro B", "preco": 45}
    ]
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": produtos})

E no template produtos.html:
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <h1>Produtos</h1>
  <ul>
    {% for p in produtos %}
      <li>{{ p.nome }} - R$ {{ p.preco }}</li>
    {% endfor %}
  </ul>
  <script src="/static/main.js"></script>
</body>
</html>

No SSR, qualquer ação que dependa de dados geralmente faz uma nova requisição ao servidor, que:
Recebe os parâmetros da filtragem (geralmente via query string, ?categoria=livros&preco_max=50)
Busca os dados filtrados no banco
Renderiza o template HTML novamente já com os dados filtrados
Envia o HTML pronto para o navegador
Ou seja, a página inteira é recarregada com os dados filtrados.
✅ Quando o usuário aplica um filtro, a URL muda com a query string, e o servidor envia um HTML novo com o resultado filtrado.

| Aspecto                             | SSR                                       | CSR                                                           |
| ----------------------------------- | ----------------------------------------- | ------------------------------------------------------------- |
| Filtragem                           | Recarrega a página inteira com HTML novo  | Atualiza **apenas a parte necessária** via JS, sem recarregar |
| Performance para interações rápidas | Mais lenta, cada filtro = nova requisição | Mais rápida, filtro no cliente ou via API                     |
| Complexidade do backend             | Mais simples                              | Backend precisa fornecer API JSON separada                    |

🧱 Estrutura geral de um projeto CSR
meu-projeto/
│
├─ backend/                  # API do servidor
│   ├─ app.py                # Servidor principal (FastAPI, Flask, Django REST)
│   ├─ models.py             # Modelos de dados (ex: banco)
│   ├─ routes/               # Endpoints da API
│   │   └─ produtos.py
│   └─ database/             # Banco de dados ou scripts de inicialização
│
├─ frontend/                 # Aplicação frontend
│   ├─ public/               # HTML base, favicon, index.html
│   ├─ src/
│   │   ├─ components/       # Componentes React/Vue
│   │   ├─ pages/            # Páginas da aplicação
│   │   ├─ App.js             # Arquivo principal (React)
│   │   ├─ index.js           # Entrada da aplicação
│   │   └─ styles/           # CSS ou SCSS
│   └─ package.json          # Configurações do frontend
│
└─ README.md

No backend:
from fastapi import FastAPI

app = FastAPI()

produtos = [
    {"nome": "Livro A", "preco": 30},
    {"nome": "Livro B", "preco": 45}
]

@app.get("/api/produtos")
def listar_produtos():
    return {"produtos": produtos}

No frontend (exemplo com react):
import { useEffect, useState } from "react";

function App() {
  const [produtos, setProdutos] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/produtos")
      .then(res => res.json())
      .then(data => setProdutos(data.produtos));
  }, []);

  return (
    <div>
      <h1>Produtos</h1>
      <ul>
        {produtos.map(p => (
          <li key={p.nome}>{p.nome} - R$ {p.preco}</li>
        ))}
      </ul>
    </div>
  );
}

# Schemas 
É como um contrato, uma documentação, um entendimento mútuo que deve ser estabelecido entre cliente e servidor sobre a estrutura dos dados que serão trocados. 
No universo de APIs e contratos de dados, especialmente ao trabalhar com Python, o Pydantic se destaca como uma ferramenta poderosa. Além disso, é embutido no FastAPI. A ideia dele é criar uma camada de documentação e fazer a validação dos modelos de entrada e saída da nossa API.
Ex: você define que ano deve ser do tipo INT, o Pydantic vai avaliar e não permitir algo como "mil novecentos e noventa e nove" (vai dar erro).
    

Conteúdo principal estudado:
https://youtube.com/playlist?list=PLOQgLBuj2-3KT9ZWvPmaGFQ0KjIez0403&si=g-R6HG5Nsh4XUffi
export default App;

