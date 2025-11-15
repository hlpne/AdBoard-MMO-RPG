# AdBoard MMO RPG

Серверное веб-приложение объявлений для фанатского сервера MMORPG.

## Технологический стек

- **Python 3.12+**
- **Django 5.2.x**
- **SQLite** (dev) / **PostgreSQL 15+** (prod, опционально)
- **APScheduler** для фоновых задач (опционально)
- **Markdown** для форматирования объявлений
- **Bootstrap 5** для UI (HTML/CSS only, без JavaScript)

## Установка

### Разработка (без Docker - рекомендуется для начала)

1. Создайте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate  # Windows PowerShell
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` в корне проекта (можно скопировать настройки из примера ниже):
```env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Email SMTP (настройте свои параметры или используйте для тестирования)
EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@mail.ru
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=no-reply@mmo-board.local
SERVER_EMAIL=no-reply@mmo-board.local

# Для разработки используем SQLite (по умолчанию)
# PostgreSQL не нужен, если не указаны DB_NAME, DB_USER и т.д.
```

**Важно:** Для тестирования email без реального SMTP сервера можно использовать консольный бэкенд:
```env
# В .env добавьте (или измените в settings.py напрямую):
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
Письма будут выводиться в консоль вместо отправки.

4. Создайте директорию для логов:
```bash
mkdir logs
```

5. Выполните миграции:
```bash
python manage.py migrate
```

6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустите сервер:
```bash
python manage.py runserver
```

Откройте браузер: http://127.0.0.1:8000/


## Структура проекта

```
mmo_board/
├── config/          # Настройки Django
├── accounts/        # Регистрация, авторизация, верификация email
├── adverts/         # Объявления с Markdown
├── replies/         # Отклики на объявления
├── newsletters/     # Подписки и рассылки
├── templates/       # HTML шаблоны
├── static/          # Статические файлы (CSS)
├── media/           # Загруженные файлы


## Основные функции

- Регистрация по email с подтверждением кодом
- Создание объявлений с Markdown-форматированием
- Загрузка изображений и вставка в Markdown
- Отклики на объявления с email-уведомлениями
- Управление откликами (принять/удалить)
- Подписка на рассылки
- Административная панель для управления

## Категории объявлений

- Танки
- Хилы
- ДД
- Торговцы
- Гилдмастеры
- Квестгиверы
- Кузнецы
- Кожевники
- Зельевары
- Мастера заклинаний

## Команды управления

- `python manage.py send_newsletter` - Отправить рассылки из очереди
- `python manage.py runapscheduler` - Запустить планировщик задач

## Лицензия

MIT

