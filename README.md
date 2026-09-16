# goit-cs-hw-03. PostgreSQL система управління завданнями + MongoDB CRUD

## Завдання 1 — task1

PostgreSQL база даних для системи управління завданнями (users, status, tasks).

Файли:
- `create_tables.sql` — створення таблиць + базові статуси (new, in progress, completed)
- `seed.py` — заповнення users і tasks випадковими даними через Faker
- `queries.sql` — усі 14 обов'язкових запитів із завдання

Запуск (PostgreSQL піднятий локально через Docker):
```
docker run --name hw03-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
docker exec -it hw03-postgres psql -U postgres -c "CREATE DATABASE task_manager;"

cd task1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

PGPASSWORD=postgres psql -h localhost -U postgres -d task_manager -f create_tables.sql
python3 seed.py
PGPASSWORD=postgres psql -h localhost -U postgres -d task_manager -f queries.sql
```

Параметри підключення (host/user/password) — на початку `seed.py` у словнику `DB_CONFIG`, підправ під свої.

## Завдання 2 — task2

Python-скрипт `main.py` з CRUD-операціями над колекцією `cats` у MongoDB через PyMongo.
Консольне меню: показати всіх котів, знайти за ім'ям, оновити вік, додати характеристику,
видалити одного / видалити всіх. При першому запуску на порожній колекції автоматично
додає 3 приклади котів, щоб було з чим одразу працювати.

Запуск (MongoDB піднятий локально через Docker):
```
docker run --name hw03-mongo -p 27017:27017 -d mongo:7

cd task2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

За замовчуванням підключається до `mongodb://localhost:27017/` (див. `MONGO_URI` у main.py)