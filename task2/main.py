"""
main.py

CRUD-операції над колекцією котів у MongoDB за допомогою PyMongo.

Структура документа:
{
    "_id": ObjectId(...),
    "name": "barsik",
    "age": 3,
    "features": ["ходить в капці", "дає себе гладити", "рудий"]
}
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "cats_db"
COLLECTION_NAME = "cats"


def get_collection(client=None):
    """Повертає колекцію cats. Якщо клієнт не переданий, підключається сам."""
    if client is None:
        client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


# ---------- Create (допоміжна функція, щоб було з чим працювати) ----------

def seed_sample_cats(collection):
    """Додає кілька прикладових котів, якщо колекція порожня."""
    if collection.count_documents({}) > 0:
        return
    sample_cats = [
        {"name": "barsik", "age": 3, "features": ["ходить в капці", "дає себе гладити", "рудий"]},
        {"name": "murka", "age": 5, "features": ["любить спати", "сіра", "полює на мишей"]},
        {"name": "vasyl", "age": 1, "features": ["грайливий", "чорний", "боїться води"]},
    ]
    try:
        collection.insert_many(sample_cats)
        print(f"Додано {len(sample_cats)} прикладових записів.")
    except PyMongoError as e:
        print(f"Помилка при додаванні прикладових даних: {e}")


# ---------- Read ----------

def print_all_cats(collection):
    """Виводить усі записи з колекції."""
    try:
        cats = list(collection.find())
        if not cats:
            print("У колекції немає жодного запису.")
            return
        for cat in cats:
            print(cat)
    except PyMongoError as e:
        print(f"Помилка при отриманні записів: {e}")


def find_cat_by_name(collection, name=None):
    """Запитує ім'я кота (якщо не передане) і виводить інформацію про нього."""
    if name is None:
        name = input("Введіть ім'я кота: ").strip()
    try:
        cat = collection.find_one({"name": name})
        if cat is None:
            print(f"Кота з ім'ям '{name}' не знайдено.")
        else:
            print(cat)
    except PyMongoError as e:
        print(f"Помилка при пошуку кота: {e}")


# ---------- Update ----------

def update_cat_age(collection, name=None, age=None):
    """Оновлює вік кота за ім'ям."""
    if name is None:
        name = input("Введіть ім'я кота, вік якого потрібно оновити: ").strip()
    if age is None:
        age = input("Введіть новий вік: ").strip()
    try:
        age = int(age)
    except ValueError:
        print("Вік має бути цілим числом.")
        return
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": age}})
        if result.matched_count == 0:
            print(f"Кота з ім'ям '{name}' не знайдено.")
        else:
            print(f"Вік кота '{name}' оновлено на {age}.")
    except PyMongoError as e:
        print(f"Помилка при оновленні віку: {e}")


def add_cat_feature(collection, name=None, feature=None):
    """Додає нову характеристику до списку features кота за ім'ям."""
    if name is None:
        name = input("Введіть ім'я кота: ").strip()
    if feature is None:
        feature = input("Введіть нову характеристику: ").strip()
    try:
        result = collection.update_one(
            {"name": name}, {"$addToSet": {"features": feature}}
        )
        if result.matched_count == 0:
            print(f"Кота з ім'ям '{name}' не знайдено.")
        else:
            print(f"Характеристику '{feature}' додано коту '{name}'.")
    except PyMongoError as e:
        print(f"Помилка при додаванні характеристики: {e}")


# ---------- Delete ----------

def delete_cat_by_name(collection, name=None):
    """Видаляє запис із колекції за ім'ям тварини."""
    if name is None:
        name = input("Введіть ім'я кота, якого потрібно видалити: ").strip()
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count == 0:
            print(f"Кота з ім'ям '{name}' не знайдено.")
        else:
            print(f"Кота '{name}' видалено.")
    except PyMongoError as e:
        print(f"Помилка при видаленні кота: {e}")


def delete_all_cats(collection):
    """Видаляє всі записи з колекції."""
    try:
        result = collection.delete_many({})
        print(f"Видалено записів: {result.deleted_count}.")
    except PyMongoError as e:
        print(f"Помилка при видаленні всіх записів: {e}")


# ---------- Меню ----------

MENU = """
Оберіть дію:
1 - Показати всіх котів
2 - Знайти кота за ім'ям
3 - Оновити вік кота
4 - Додати характеристику коту
5 - Видалити кота за ім'ям
6 - Видалити всіх котів
0 - Вихід
"""


def main():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")
    except PyMongoError as e:
        print(f"Не вдалося підключитись до MongoDB за адресою {MONGO_URI}: {e}")
        return

    collection = get_collection(client)
    seed_sample_cats(collection)

    actions = {
        "1": lambda: print_all_cats(collection),
        "2": lambda: find_cat_by_name(collection),
        "3": lambda: update_cat_age(collection),
        "4": lambda: add_cat_feature(collection),
        "5": lambda: delete_cat_by_name(collection),
        "6": lambda: delete_all_cats(collection),
    }

    while True:
        print(MENU)
        choice = input("Ваш вибір: ").strip()
        if choice == "0":
            print("Вихід із програми.")
            break
        action = actions.get(choice)
        if action is None:
            print("Невірний вибір, спробуйте ще раз.")
            continue
        action()


if __name__ == "__main__":
    main()
