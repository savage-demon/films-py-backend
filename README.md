# Films API

Read-only REST API для просмотра фильмов из готовой базы Sakila.

## Стек

- Python 3.13, [uv](https://docs.astral.sh/uv/)
- FastAPI, Uvicorn
- SQLAlchemy 2 async
- MySQL Sakila database

## Быстрый старт

```bash
cp .env.example .env
# укажите в .env подключение к готовой Sakila-базе
make bootstrap
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## API

Базовый prefix: `/v1`.

### `GET /v1/films/search-meta`

Данные для формы поиска перед вводом пользователем:

- список всех жанров из `category`
- минимальный год выпуска фильмов
- максимальный год выпуска фильмов

Ответ:

```json
{
  "genres": ["Action", "Comedy"],
  "min_release_year": 2005,
  "max_release_year": 2012
}
```

### `GET /v1/films/`

Список фильмов. Размер страницы по умолчанию: 10 фильмов. Его можно изменить параметром `size`. Следующие результаты запрашиваются через `page=2`, `page=3` и так далее.

Фильтры:

| Параметр | Описание |
|----------|----------|
| `keyword` | Поиск по названию фильма |
| `title` | Алиас для поиска по названию |
| `genre` | Точное имя жанра из `category.name` |
| `year` | Конкретный год выпуска |
| `year_from` | Нижняя граница года выпуска |
| `year_to` | Верхняя граница года выпуска |
| `page` | Номер страницы, по умолчанию `1` |
| `size` | Размер страницы, по умолчанию `10`, максимум `100` |

Сортировка: `order_by` (`title`, `-title`, `release_year`, `-release_year`), по умолчанию `title`.

Примеры:

```text
GET /v1/films/?keyword=academy&page=1&size=10
GET /v1/films/?genre=Comedy&year_from=2005&year_to=2012&page=2&size=20
GET /v1/films/?genre=Drama&year=2006
```

Ответ:

```json
{
  "items": [
    {
      "id": 1,
      "title": "ACADEMY DINOSAUR",
      "description": "...",
      "release_year": 2006,
      "genres": ["Documentary"]
    }
  ],
  "total": 12,
  "page": 1,
  "size": 10,
  "pages": 2
}
```

### `GET /v1/films/{film_id}`

Один фильм по `film.film_id`. При отсутствии возвращает `404`.

## Локальная разработка без Docker

```bash
uv sync
uv run fastapi dev src/main.py
```
