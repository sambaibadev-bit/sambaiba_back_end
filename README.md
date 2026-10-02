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
python -m venv venv
source venv/bin/activate
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

### 5. (Opcional) Povoar dados de demonstração

Com o banco migrado e o servidor podendo conectar ao Postgres:

```powershell
python manage.py seed_sambaiba
```

Isso insere eventos, galeria, campanhas, notícias, contatos e sugestões de exemplo. Linhas antigas criadas pelo mesmo comando são removidas antes (identificador `[Seed] ` no título/nome). Use `--skip-suggestions` para não criar sugestões de teste.

Também garante um administrador local para o painel do site e para o Django admin. Rodar de novo redefine a senha desse usuário. Os demais usuários não são alterados.

- E-mail: `admin@sambaiba.local`
- Senha: `sambaiba123`

### 6. Servidor de desenvolvimento

```powershell
python manage.py runserver
```

A API fica em `http://127.0.0.1:8000/`.

- **Swagger UI (testar a API):** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/) (espelho: [http://127.0.0.1:8000/api/swagger/](http://127.0.0.1:8000/api/swagger/)) — textos da documentação OpenAPI em **inglês**
- **Schema OpenAPI (JSON):** [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)
- **ReDoc:** [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **Admin Django:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Estrutura útil

- `config/` — settings e URLs principais
- `apps/` — apps Django (`users`, `jwt_auth`, `events`, `actions`, …)
- `api/` — rotas agregadas sob `/api/`
- `core/` — paginação, permissões, utilitários OpenAPI e validadores compartilhados

## Produção

Defina as mesmas variáveis de Postgres (e `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`) no ambiente do provedor, sem commitar `.env`.
