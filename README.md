# EP_Skypro5 - Учебный проект по Django

Это учебный проект, созданный в рамках изучения Django. Проект представляет собой веб-приложение с базовыми функциями, реализованными для освоения фреймворка.

## Технологии и библиотеки

- Python 3.11 (использовалась версия 3.11.x)
- Django 4.2.x
- Дополнительные зависимости указаны в файле `requirements.txt`

## Установка и запуск проекта

1. Клонируйте репозиторий:
   
       git clone https://github.com/Arty525/EP_Skypro5.git
       cd EP_Skypro5

3. Создайте и активируйте виртуальное окружение (для Windows/Linux):

    Для Windows

        python -m venv venv
        venv\Scripts\activate

    Для Linux/macOS
   
        python3 -m venv venv
        source venv/bin/activate
   
5. Установите зависимости:

       pip install -r requirements.txt
   
7. Создайте базу данных PostgreSQL и примените миграции:

       python manage.py migrate
   
9. Запустите сервер разработки:

        python manage.py runserver

## Кастомные команды
Проект включает следующие пользовательские команды:

python manage.py <название_команды>

Доступные команды:

    add_users - добавить тестовых пользователей
    add_courses - добавить тестовые курсы
    add_lessons - добавить тестовые уроки
    add_payments - добавить тестовые платежные операции
    add_users_into_group - добавить пользователей в группы