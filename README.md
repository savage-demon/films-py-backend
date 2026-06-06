# Films API

Read-only REST API каталога фильмов на FastAPI.

Фронтенд: [films_frontend](../films_frontend/).

## Стек

- Python 3.13, [uv](https://docs.astral.sh/uv/)
- FastAPI, Uvicorn
- SQLAlchemy 2 (async), asyncpg
- PostgreSQL 17
- Alembic
- fastapi-pagination

## Быстрый старт (Docker)

```bash
cp .env.example .env
task up
task db:migrate
task db:seed    # опционально, 300 тестовых фильмов
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- PostgreSQL с хоста: `localhost:6932` (user/pass/films)

## Taskfile

| Команда | Описание |
|---------|----------|
| `task net:create` | Создать Docker-сеть `ichub_films_net` |
| `task up` | Поднять контейнеры |
| `task down` | Остановить контейнеры |
| `task logs` | Логи приложения |
| `task db:migrate` | Применить миграции |
| `task db:mm 'msg'` | Создать миграцию (alias `db:makemigration`) |
| `task db:seed` | Заполнить БД тестовыми данными |

## API

Базовый prefix: `/v1`.

### `GET /v1/films/`

Список фильмов с пагинацией.

**Пагинация:** `page`, `size`

**Фильтры:**

| Параметр | Описание |
|----------|----------|
| `title` | Поиск по названию (ILIKE) |
| `genre` | Поиск по жанру (ILIKE) |
| `rating_gte` | Рейтинг ≥ |
| `rating_lte` | Рейтинг ≤ |
| `release_date__gte` | Дата выхода ≥ |

**Сортировка:** `order_by` (по умолчанию `title`)

`title`, `-title`, `rating`, `-rating`, `release_date`, `-release_date`

**Ответ:** `{ items, total, page, size, pages }`

### `GET /v1/films/{film_id}`

Один фильм. При отсутствии — `404`.

### Модель `FilmResponse`

`id`, `title`, `description`, `release_date`, `rating`, `genre`

## Переменные окружения

См. [`.env.example`](.env.example):

| Переменная | Описание |
|------------|----------|
| `APP_TITLE` | Заголовок API |
| `APP_VERSION` | Версия |
| `DEBUG` | Режим отладки |
| `DB_URL` | Строка подключения PostgreSQL (asyncpg) |
| `CORS_ORIGINS` | Origins для CORS (JSON-массив в `.env`) |

## Docker-сеть с фронтендом

Backend и frontend используют external-сеть `ichub_films_net`.

Контейнер API доступен фронту по имени `app:8000`.

```bash
task net:create   # один раз
task up
```

Затем поднять [films_frontend](../films_frontend/) (`task up` в его каталоге).

## Локальная разработка без Docker

```bash
uv sync
uv run alembic upgrade head
uv run python -m src.seeder
uv run fastapi dev src/main.py
```

PostgreSQL должен быть доступен по `DB_URL` из `.env`.

## Структура проекта

```
films/
├── src/
│   ├── main.py              # точка входа FastAPI
│   ├── config.py            # настройки
│   ├── database.py          # async engine / session
│   ├── api/v1/films.py      # роуты
│   ├── services/film.py     # бизнес-логика
│   ├── query_builders/      # сборка SQL-запросов
│   ├── models/              # SQLAlchemy-модели
│   ├── schemas/             # Pydantic-схемы
│   └── exceptions/          # обработка ошибок
├── migrations/              # Alembic
├── deployment/              # Dockerfile
├── docker-compose.yml
└── Taskfile.yml
```
