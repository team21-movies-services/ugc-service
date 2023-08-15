# ugc-service

* link = https://github.com/team21-movies-services/ugc-service

# Стек технологий
- Frontend (Nginx) - маршрутизация запросов
- Backend (Fastapi) - получение и обработка запросов пользователя

## backend библиотеки
* `fastapi` - основной backend фреймворк
* `pydantic` - валидация входящих данных api
* `uvicorn` - локальный запуск проекта, `gunicorn` - запуск в прод. окружении
* `pyjwt` - библиотека для работы с jwt


### Линтеры
* flake8, mypy, bandit

# Init development

1) init poetry and pre-commit
```bash
poetry install --no-root
```

```bash
poetry run pre-commit install
```

2) env
```bash
cp ./.env.template ./.env
```

```bash
cp ./src/.env.template ./src/.env
```

3) build and up docker local
```bash
make build-local
make up-local
```

4) go to `http://localhost:8000/docs`


# Init kafka

1) build and up docker local
```bash
make up-kafka
```

2) go to `http://localhost:8090`


# Perfomance tests

install dependencies

```bash
poetry install --only performance_testing   
```

## Vertica

1) run vertica

```bash
make up-vertica
```
2) wait until vertica is running

3) Run test script

```bash
poetry run python3 performance_tests/vertica.py 
```

## Mongo

1) run mongo

```bash
make up-mongo
```
2) wait until mongo is running

3) Run test script

```bash
poetry run python3 performance_tests/mongo.py 
```


# ELK

0) create .env file and change it if you want
```bash
cp ./infra/elk/.env.template ./infra/elk/.env
```

1) run elk

```bash
make up-elk
```

2) wait until elk is running

3) go to `http://localhost:5601`

login - `elastic`
password - `ES_PASSWORD` from .env

# Filebeat

## Description
Filebeat забирает логи из папки logs/nginx и logs/ugc_service по-умолчанию и передаёт их в logstash elk.

## Launch
1) run filebeat

```bash
make up-filebeat
```

2) check logs in kibana
