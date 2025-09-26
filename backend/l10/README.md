# Лабораторная работа №10 - Django проект

## Описание

Лабораторная работа по изучению Django - мощного веб-фреймворка для Python. Демонстрирует создание Django проекта с несколькими приложениями, настройку базы данных, административной панели и основные принципы MTV (Model-Template-View) архитектуры.

## Структура проекта

```
l10/
├── manage.py                    # Утилита управления Django проектом
├── my_first_django_project/     # Основная папка проекта
│   ├── __init__.py
│   ├── settings.py              # Настройки проекта
│   ├── urls.py                  # URL маршруты проекта
│   ├── wsgi.py                  # WSGI конфигурация
│   └── asgi.py                  # ASGI конфигурация
├── my_first_app/                # Первое Django приложение
│   ├── __init__.py
│   ├── admin.py                 # Конфигурация админки
│   ├── apps.py                  # Конфигурация приложения
│   ├── models.py                # Модели данных
│   ├── views.py                 # Представления (контроллеры)
│   ├── urls.py                  # URL маршруты приложения
│   ├── tests.py                 # Тесты
│   └── migrations/              # Миграции базы данных
│       └── __init__.py
├── nested_app/                  # Второе Django приложение
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── tests.py
│   └── migrations/
│       └── __init__.py
└── README.md                   # Документация (этот файл)
```

## Функциональность

### 1. Настройки проекта (`settings.py`)
- Конфигурация базы данных (SQLite)
- Установленные приложения
- Middleware настройки
- Интернационализация и локализация
- Статические файлы

### 2. Django приложения
- **my_first_app**: основное приложение с базовой функциональностью
- **nested_app**: дополнительное приложение для демонстрации модульности

### 3. MTV архитектура
- **Models**: определение структуры данных
- **Templates**: HTML шаблоны для отображения
- **Views**: бизнес-логика и контроллеры

### 4. Административная панель
- Автоматически генерируемый интерфейс администратора
- Управление пользователями и группами
- Возможность добавления собственных моделей

### 5. URL маршрутизация
- Централизованная система URL маршрутов
- Включение маршрутов из приложений
- Паттерны URL с параметрами

## Установка зависимостей

```bash
pip install Django>=5.2.6
```

## Запуск

### Применение миграций
```bash
python manage.py migrate
```

### Создание суперпользователя (опционально)
```bash
python manage.py createsuperuser
```

### Запуск сервера разработки
```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

### Доступ к административной панели
После создания суперпользователя: http://127.0.0.1:8000/admin/

## Управление проектом

### Создание нового приложения
```bash
python manage.py startapp app_name
```

### Создание миграций
```bash
python manage.py makemigrations
```

### Применение миграций
```bash
python manage.py migrate
```

### Запуск тестов
```bash
python manage.py test
```

### Сбор статических файлов
```bash
python manage.py collectstatic
```

### Django shell
```bash
python manage.py shell
```

## Основные команды

### Просмотр доступных команд
```bash
python manage.py help
```

### Проверка настроек
```bash
python manage.py check
```

### Создание дампа данных
```bash
python manage.py dumpdata > data.json
```

### Загрузка данных
```bash
python manage.py loaddata data.json
```

## Структура базы данных

По умолчанию Django создает следующие таблицы:
- `auth_user` - пользователи
- `auth_group` - группы пользователей
- `auth_permission` - права доступа
- `django_content_type` - типы контента
- `django_migrations` - история миграций
- `django_session` - сессии

## Настройки проекта

### База данных
- **ENGINE**: SQLite (по умолчанию)
- **NAME**: db.sqlite3
- Расположение: корень проекта

### Приложения
- django.contrib.admin
- django.contrib.auth
- django.contrib.contenttypes
- django.contrib.sessions
- django.contrib.messages
- django.contrib.staticfiles
- my_first_app
- nested_app

### Локализация
- **LANGUAGE_CODE**: 'en-us'
- **TIME_ZONE**: 'UTC'
- **USE_I18N**: True
- **USE_TZ**: True

## Разработка

### Добавление новых моделей
1. Определите модель в `models.py`
2. Создайте миграцию: `python manage.py makemigrations`
3. Примените миграцию: `python manage.py migrate`
4. Зарегистрируйте в админке в `admin.py`

### Создание представлений
1. Определите представление в `views.py`
2. Добавьте URL маршрут в `urls.py`
3. Создайте соответствующий шаблон

### Работа со статическими файлами
- CSS, JavaScript, изображения размещаются в папке `static/`
- Используйте `{% load static %}` в шаблонах
- Ссылайтесь на файлы через `{% static 'path/to/file' %}`

## Цель работы

Изучение Django фреймворка и принципов разработки веб-приложений на Python. Освоение MTV архитектуры, работы с базой данных через ORM, создания административного интерфейса и основ веб-разработки с использованием Django.