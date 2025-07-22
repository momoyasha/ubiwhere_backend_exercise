
# Ubiwhere Backend Exercise

Um projeto backend usando Python/Django a título de exercício.


## Requisitos
- [Docker](https://www.docker.com/)

## Instalação
Clone o projeto com:

```bash
  git clone https://github.com/momoyasha/ubiwhere_backend_exercise.git
```
Ou faça download como .zip e extraia em algum diretório.

É necessário criar um arquivo .env na raíz do projeto com as seguintes chaves:

```
POSTGRES_USER=nome de usuário
POSTGRES_PASSWORD=senha
POSTGRES_DB=nome da base de dados
```
A base de dados será criada via docker-compose utilizando essas variáveis, que também serão usadas pelo Django para estabelecer a conexão.


Em um prompt de comando na pasta raíz do projeto, execute:
```
  docker compose build --no-cache
  docker-compose up
```
    
Isso vai criar um projeto com dois containeres, um para a base de dados em PostgreSQL (PostGIS) e um para o servidor Django.

A partir daí, você pode rodar:
```
  docker exec -it django-dev sh
```

Para rodar comandos dentro do container. E então:
```
  python backend/manage.py createsuperuser
```
Para criar o primeiro usuário (com privilégios de administrador).

Com isso, é possível acessar o Django Admin para criar usuários usando a interface de usuário, além de emitir tokens de autenticação pelos endpoints correspondentes.
## Uso geral

O servidor é acessível via http://localhost:8000/.

O painel de administração fica em http://localhost:8000/admin. Use as credenciais do super usuário criado acima.

Uma documentação mais detalhada das APIs disponíveis pode ser encontrada em http://localhost:8000/api/docs.

Endpoints usando métodos POST, PUT e DELETE são apenas acessíveis com permissão de administrador. É necessário passar um token de acesso correspondente para acessá-los.
