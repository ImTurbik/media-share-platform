# МемХостинг

Простое учебное приложение для публикации мемов и картинок.  
Можно выкладывать посты, лайкать их, писать комментарии, открывать профиль пользователя и делиться ссылкой на конкретный пост.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D?logo=vuedotjs&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

## Что умеет

| Возможность       | Что делает                                                  |
|-------------------|-------------------------------------------------------------|
| Лента постов      | Показывает все публикации в одном месте                     |
| Профиль           | Отдельная страница с постами конкретного пользователя       |
| Один пост         | Открывает конкретную публикацию по ссылке                   |
| Лайки             | Можно поставить лайк и снять его                            |
| Список лайкнувших | Под постом показываются никнеймы тех, кто уже поставил лайк |
| Комментарии       | Можно добавлять и удалять только свои комментарии           |
| Удаление постов   | Автор может удалить только свой пост                        |
| Ссылка на пост    | У каждого поста есть кнопка для копирования прямой ссылки   |
| Просмотр фото     | Картинки открываются в увеличенном виде                     |

## Технологии

| Часть проекта   | Стек                          |
|-----------------|-------------------------------|
| Фронтенд        | `Vue 3`, `Vite`, `Vue Router` |
| Бэкенд          | `FastAPI`, `SQLAlchemy`       |
| База данных     | `PostgreSQL`                  |
| Стили           | `Tailwind CSS`                |
| Контейнеризация | `Docker`, `Docker Compose`    |

## Требования

| Для запуска         | Нужно                       |
|---------------------|-----------------------------|
| Через Docker        | `Docker` + `Docker Compose` |
| Локально без Docker | `Python 3.11+`, `Node.js`   |

## Запуск

### Через Docker

```bash
docker compose up --build
```

После запуска:

| Сервис   | Адрес                        |
|----------|------------------------------|
| Frontend | `http://localhost:5173`      |
| Backend  | `http://localhost:8000`      |
| Swagger  | `http://localhost:8000/docs` |

### Без Docker

#### Backend

```bash
cd backend
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev -- --host
```

## Конфигурация

Адрес API задаётся в файле:

- `frontend/src/config.js`

По умолчанию используется:

```js
http://localhost:8000
```


## API

| Эндпоинт                                            | Что делает                  |
|-----------------------------------------------------|-----------------------------|
| `GET /api/posts`                                    | Получить ленту постов       |
| `GET /api/posts/{post_id}`                          | Получить конкретный пост    |
| `GET /api/users/{author_name}/posts`                | Получить посты пользователя |
| `POST /api/posts`                                   | Создать пост                |
| `DELETE /api/posts/{post_id}`                       | Удалить свой пост           |
| `POST /api/posts/{post_id}/like`                    | Поставить лайк              |
| `POST /api/posts/{post_id}/unlike`                  | Снять лайк                  |
| `GET /api/posts/{post_id}/likes`                    | Посмотреть, кто лайкнул     |
| `POST /api/posts/{post_id}/comments`                | Добавить комментарий        |
| `DELETE /api/posts/{post_id}/comments/{comment_id}` | Удалить свой комментарий    |
| `GET /api/posts/{post_id}/comments`                 | Получить комментарии поста  |

## Лицензия

Проект распространяется под MIT License.
