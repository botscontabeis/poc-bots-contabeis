# Bots Contabeis

Plataforma para execução de bots contábeis.

## Bots Disponíveis

- Consulta de Domicílio Tributário Eletrônico na UVT-RN;

## Executando Localmente

1. Clone este repositório;
2. Crie um ambiente virtual e instale as dependências:
```shell
$ python -m venv venv
$ pip install -r requirements.txt
```
3. Crie o arquivo `.env` a partir do `.env.example` preenchendo os valores da variáveis de acordo com seu ambiente:
```shell
$ cp .env.example .env
```
4. Utilizando Docker Compose, inicialize a infraestrutura:
```shell
$ docker compose up -d
```
5. Inicialize o worker `celery`:
```shell
$ celery -A botscontabeis worker -l INFO
```
6. Rode as migrações, crie um super usuário e inicialize o servidor `Django`:
```shell
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

## Executando os Testes

```shell
$ pytest
```
