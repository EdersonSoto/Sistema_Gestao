# Sistema de Gestão

Base inicial do projeto web **Sistema de Gestão**, desenvolvido pela **Soto Company**.

Esta etapa cria a fundação do projeto:

- Backend com **FastAPI**
- Frontend inicial com **HTML, CSS, JavaScript e Bootstrap 5**
- Estrutura preparada para evoluir para **PostgreSQL**
- Organização pensada para módulos futuros como clientes, equipamentos, ordens de serviço e estoque

## 1. O que é o Sistema de Gestão

O Sistema de Gestão será uma aplicação web empresarial para centralizar operações internas da empresa, como acompanhamento de clientes, equipamentos, ordens de serviço, estoque, compras, relatórios e permissões de usuários.

## 2. Tecnologias utilizadas

- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Python
- FastAPI
- SQLAlchemy
- SQLite para desenvolvimento inicial
- PostgreSQL como banco principal futuro
- Hash seguro de senha com PBKDF2
- Token assinado para login
- Perfis de acesso por função

## 3. Estrutura de diretórios

```text
sistema-gestao/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── run_backend.bat
│   └── app/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── database.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── system_info.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── auth.py
│       └── api/
│           ├── __init__.py
│           └── routes/
│               ├── __init__.py
│               ├── auth.py
│               └── health.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── database/
├── docs/
├── .gitignore
└── README.md
```

## 4. Como instalar as dependências

Crie e ative um ambiente virtual, depois instale os pacotes do backend:

```bash
cd backend
pip install -r requirements.txt
```

## 5. Como iniciar o backend

No diretório `backend`, execute:

```bash
uvicorn main:app --reload
```

Ou, no Windows, dê duplo clique em `backend/run_backend.bat`.

O backend ficará disponível em:

- API: `http://127.0.0.1:8000`
- Documentação automática Swagger: `http://127.0.0.1:8000/docs`
- Documentação alternativa: `http://127.0.0.1:8000/redoc`

## 6. Como acessar o sistema pelo navegador

Abra `http://127.0.0.1:8000/` com o backend rodando.

## 7. Como testar a API

Com o backend em execução, acesse:

```bash
GET /api/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "system": "Sistema de Gestão",
  "version": "1.0.0"
}
```

## 8. Próximos passos planejados

- Criar mais modelos de banco para os módulos futuros
- Incluir migrações de banco de dados
- Estruturar módulos de clientes, equipamentos e ordens de serviço
- Implementar autenticação e controle de permissões
- Separar camadas de aplicação com mais organização
- Evoluir o frontend para consumir a API via HTTP/JSON

## Entendendo a base

- **FastAPI** é um framework Python para criar APIs de forma rápida e organizada.
- **API** é a interface que permite a comunicação entre o navegador e o backend.
- **Endpoint** é uma rota específica da API, como `/api/health`.
- **JSON** é um formato leve de dados usado para trocar informações entre frontend e backend.
