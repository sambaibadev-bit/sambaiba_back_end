# sambaiba_back_end

API REST em **Django** e **Django REST Framework**, com autenticação **JWT**, documentação **OpenAPI/Swagger** e banco **PostgreSQL**.

## Pré-requisitos

- Python 3.12+ (o projeto foi testado com 3.13)
- PostgreSQL em execução (local ou remoto)

## Como iniciar o projeto

### 1. Ambiente virtual e dependências

Na raiz do repositório:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Variáveis de ambiente

Copie o exemplo e ajuste credenciais e host do Postgres:

```powershell
copy .env.example .env
```

Edite `.env` conforme seu PostgreSQL (veja variáveis em `.env.example`).

### 3. Banco de dados

Crie o banco e o usuário no PostgreSQL (exemplo — ajuste nomes e senha):

```sql
CREATE USER sambaiba WITH PASSWORD 'sambaiba';
CREATE DATABASE sambaiba OWNER sambaiba;
```

### 4. Migrações e (opcional) superusuário

```powershell
python manage.py migrate
python manage.py createsuperuser
```

### 5. Servidor de desenvolvimento

```powershell
python manage.py runserver
```

A API fica em `http://127.0.0.1:8000/`.

- **Swagger (testar a API):** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **ReDoc:** [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **Admin Django:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Estrutura útil

- `config/` — settings e URLs principais
- `apps/` — apps Django (`users`, `jwt_auth`, `events`, `actions`, …)
- `api/` — rotas agregadas sob `/api/`
- `core/` — paginação, permissões e validadores compartilhados

## Produção

Defina as mesmas variáveis de Postgres (e `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`) no ambiente do provedor, sem commitar `.env`.
