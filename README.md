# Благотворительный фонд поддержки котиков QRKot
Фонд собирает пожертвования на различные целевые проекты

### Используемые технологии:

+ Python
+ FastAPI
+ SQLAlchemy
+ Pydantic
+ Uvicorn
+ Alembic
+ Aiogoogle

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
>>> git clone https://github.com/Ponimon4ik/cat_charity_fund
```

```
>>> cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
>>> python3 -m venv venv
```

* Если у вас Linux/MacOS
    ```
    >>> source venv/bin/activate
    ```
* Если у вас windows

    ```
    >>> source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
>>> python3 -m pip install --upgrade pip
```
```
>>> pip install -r requirements.txt
```
Cоздать env-файл и прописать переменные окружения в нём:
```
>>> touch .env
```
В проекте есть файл заготовка env_blank
```
DATABASE_URI= dialect+driver://username:password@host:port/database # расположение базы данных
SECRET_KEY= secret_key # секретный ключ приложения
FIRST_SUPERUSER_EMAIL=admin@mail.ru # почтовый адресс первого суперюзера
FIRST_SUPERUSER_PASSWORD=admin # пароль для уч. записи первого суперюзера
```
Для создания БД, выполните следующие команду:
```
>>> alembic upgrade head
```

Что бы запустить приложение выполните команду:

```
>>> uvicorn app.main:app --reload 
```
При первом запуске приложения суперюзер создается автоматически
на основании данных для первого суперюзера из .env

### Автор:

+ [Стефанюк Богдан](https://github.com/Ponimon4ik)