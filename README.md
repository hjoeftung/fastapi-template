Шаблон сервиса на FastAPI

## Запуск проекта
```shell
# если poetry не установлена, ее можно скачать:
# https://python-poetry.org/docs/#installation

# устанавливаем зависимости
poetry install

# поднимаем postgres
make db

# накатываем миграции
make migrate

# запускаемся на 8000 порту
make run
```

## Запуск тестов

```shell
# паралллельный запуск в 4 процесса
make test

# запуск в 1 процесс
poetry run pytest src
```
