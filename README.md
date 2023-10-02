# VICTORY_GROUP_TEST

## Описание

Этот бот предназначен для отправки сообщений пользователям.

## Технологии

- Python 3.x
- aiogram
- Celery
- Redis
- PostgreSQL
- Docker

## Установка и запуск

Перед началом убедитесь, что у вас установлены Docker и Docker Compose.

### 1. Клонирование репозитория

```bash
git clone https://github.com/ValeraTheSlayer/aiogram_bot.git
cd [Имя папки репозитория]
```

### 2. Настройка переменных окружения

Создайте файл .env в корневой директории проекта и добавьте в него следующие переменные:

```bash
BOT_TOKEN=токен бота из телеги
POSTGRES_DB=имя_базы_данных
POSTGRES_USER=имя_пользователя
POSTGRES_PASSWORD=пароль
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_URL=redis://redis:6379/0
```

### 3. Настройка переменных окружения

```angular2html
docker-compose up --build
```


## После выполнения этих команд, ваш бот должен быть запущен и работать.

## Использование

- `/start` - Начало работы бота
- `/create` - Создание сообщения для рассылки
- `/schedule` - Сохранение в шаблон для рассылки

## Структура проекта

- `/app` - основная папка с кодом
  - `/handlers` - обработчики событий и команд
  - `/models` - модели базы данных
  - `/tasks` - фоновые задачи (Celery)
- `/configs` - конфигурационные файлы
- `docker-compose.yml` - файл для Docker Compose
- `celery_app.py` - Инициализация Celery
- `celery_config.py` - Настройка Celery
- `Dockerfile` - Dockerfile
- `main.py` - точка входа в приложение
- `.env` - файл с переменными окружения (не добавлять в репозиторий!)
- `README.md` - этот файл
