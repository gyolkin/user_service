# User Service

![Главный баннер](./docs/banner.png)

<center>

![Python 3.10](https://img.shields.io/badge/Python-3.10-green?style=flat&logo=python&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-purple?style=flat&logo=poetry&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

</center>

User Service - простая ботоферма, которая отдает реальные учетные данные пользователя по требованию для использования в E2E-тестах.

Стек приложения:
- Python
  - FastAPI
  - Pydantic
  - SQLAlchemy & alembic
  - Dishka (DI framework)
- PostgreSQL

Чтобы начать работу, клонируйте данный репозиторий и перейдите в корневую директорию приложения.

## Локальный запуск
Используется пакетный менеджер Poetry. Чтобы установить зависимости, выполните следующую команду:
```bash
poetry install
```

Активируйте виртуальное окружение:
```bash
poetry shell
```

Примените последнюю версию базы данных. Для локальной разработки будет создана ```dev.db``` база данных, использующая SQLite:
```bash
alembic upgrade head
```

Запустите приложение:
```bash
uvicorn src.user_service.main:create_production_app
```

Вы можете начать пользоваться приложением через [интерактивную документацию](http://127.0.0.1:8000/docs).

## Запуск с помощью Docker
Для запуска приложения в production-ready окружении создайте ```.env``` файл по образцу [.env.example](.env.example). Выполните команду:
```bash
docker compose up --build -d
```

Вы можете начать пользоваться приложением через [интерактивную документацию](http://127.0.0.1:8000/docs).

## Тестирование
Предполагается, что вы выполнили все шаги из раздела [Локальный запуск](#локальный-запуск).

Приложение покрыто тестами. Для запуска тестов используйте команду:
```bash
pytest -l
```

При необходимости создайте coverage-репорт в удобном формате:
```bash
pytest --cov=src/user_service --cov-report html
```
