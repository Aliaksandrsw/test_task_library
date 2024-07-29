# Управления библиотекой

Это Django-приложение представляет собой  управление библиотекой, которое позволяет читателям просматривать каталог книг, брать их и возвращать. 
Оно включает в себя RESTful API и использует Django Simple History для отслеживания изменений.

## Функциональность

- Просмотр каталога книг
- Возможность брать и возвращать книги
- Отслеживать должников
- RESTful API для программного доступа
- Отслеживание истории изменений с помощью Django Simple History

## Установка

1. Клонируйте репозиторий: git clone https://github.com/Aliaksandrsw/test_task_library
2. Перейдите в папку с проектом cd test_task_library
3. Создайте виртуальное окружение и активируйте его:
python -m venv venv
source venv/bin/activate  # На Windows используйте venv\Scripts\activate
4. Установите необходимые пакеты: pip install -r requirements.txt
5. Примените миграции базы данных: python manage.py migrate
6. Запустите сервер разработки: python manage.py runserver
7. Перейдите по адресу http://127.0.0.1:8000/
