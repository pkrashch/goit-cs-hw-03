"""
seed.py

Заповнює таблиці users, status та tasks випадковими даними
за допомогою бібліотеки Faker.
"""

import random

import psycopg2
from faker import Faker

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "task_manager",
    "user": "postgres",
    "password": "postgres",
}

NUM_USERS = 20
NUM_TASKS = 60

fake = Faker()


def seed_status(cur):
    """Гарантуємо наявність базових статусів (не дублюємо, якщо вже є)."""
    statuses = ["new", "in progress", "completed"]
    for name in statuses:
        cur.execute(
            "INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
            (name,),
        )


def seed_users(cur, n):
    """Створює n випадкових користувачів і повертає список їхніх id."""
    user_ids = []
    for _ in range(n):
        fullname = fake.name()
        email = fake.unique.email()
        cur.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id",
            (fullname, email),
        )
        user_ids.append(cur.fetchone()[0])
    return user_ids


def seed_tasks(cur, n, user_ids, status_ids):
    """Створює n випадкових завдань, прив'язаних до випадкових користувачів і статусів.

    Частина завдань навмисно залишається без опису (description = NULL),
    щоб можна було продемонструвати відповідний запит.
    """
    for _ in range(n):
        title = fake.sentence(nb_words=4).rstrip(".")
        description = fake.paragraph(nb_sentences=3) if random.random() > 0.2 else None
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cur.execute(
            """
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, %s, %s)
            """,
            (title, description, status_id, user_id),
        )


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn:
            with conn.cursor() as cur:
                seed_status(cur)

                cur.execute("SELECT id FROM status ORDER BY id")
                status_ids = [row[0] for row in cur.fetchall()]

                user_ids = seed_users(cur, NUM_USERS)

                # Свідомо залишаємо кілька користувачів без завдань,
                # щоб запит "користувачі без завдань" завжди мав що показати.
                users_with_tasks = user_ids[:-3]
                seed_tasks(cur, NUM_TASKS, users_with_tasks, status_ids)

        print(f"Готово: додано {NUM_USERS} користувачів і {NUM_TASKS} завдань.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
