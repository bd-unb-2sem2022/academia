# gymApp

Aplicação web CRUD para sistema de academia desenvolvida com Django

## Estrutura

- `gymApp`: configurações globais
- `app`: aplciação web da academia
    - `templates`: paginas do app
    - `static`: arquivos de media, css, js... 

## Setup

```sh
    pip install -r requirements.txt
```

## Dados

- admin:
    - username: gymapp
    - password: bd2022

### conexão com o banco

A configuração é feita no arquivo [gymApp/settings.py](./gymApp/settings.py) na linha 79.

### Sincronizando com o banco
```sh
    python3 manage.py makemigrations
    python3 manage.py make migrate
```

## Run
```sh
    python3 manage.py runserver
```

- acesse http://localhost:8000
