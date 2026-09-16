-- queries.sql
-- Набір запитів до бази даних системи управління завданнями.
-- Конкретні id/значення підставлені для прикладу під seed-дані з seed.py,
-- за потреби зміни їх на свої.

-- 1. Отримати всі завдання певного користувача (user_id = 13)
SELECT *
FROM tasks
WHERE user_id = 13;

-- 2. Вибрати завдання з конкретним статусом (наприклад, 'new') через підзапит
SELECT *
FROM tasks
WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- 3. Оновити статус конкретного завдання (id = 60) на 'in progress'
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 60;

-- 4. Отримати користувачів, які не мають жодного завдання
SELECT *
FROM users
WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);

-- 5. Додати нове завдання для конкретного користувача (user_id = 13)
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'Нове тестове завдання',
    'Опис нового завдання, доданого запитом 5',
    (SELECT id FROM status WHERE name = 'new'),
    13
);

-- 6. Отримати всі завдання, які ще не завершено (статус != 'completed')
SELECT *
FROM tasks
WHERE status_id <> (SELECT id FROM status WHERE name = 'completed');

-- 7. Видалити конкретне завдання (id = 59)
DELETE FROM tasks
WHERE id = 59;

-- 8. Знайти користувачів з певною електронною поштою (тут: усі на example.com)
SELECT *
FROM users
WHERE email LIKE '%@example.com';

-- 9. Оновити ім'я користувача (id = 13)
UPDATE users
SET fullname = 'Claudia Ellis-Smith'
WHERE id = 13;

-- 10. Кількість завдань для кожного статусу
SELECT s.name, COUNT(t.id) AS tasks_count
FROM status s
LEFT JOIN tasks t ON t.status_id = s.id
GROUP BY s.name;

-- 11. Завдання користувачів з певним доменом пошти (example.com)
SELECT t.*
FROM tasks t
JOIN users u ON u.id = t.user_id
WHERE u.email LIKE '%@example.com';

-- 12. Завдання без опису
SELECT *
FROM tasks
WHERE description IS NULL;

-- 13. Користувачі та їхні завдання зі статусом 'in progress'
SELECT u.id, u.fullname, t.id AS task_id, t.title
FROM users u
INNER JOIN tasks t ON t.user_id = u.id
INNER JOIN status s ON s.id = t.status_id
WHERE s.name = 'in progress';

-- 14. Користувачі та кількість їхніх завдань (включно з тими, у кого 0)
SELECT u.id, u.fullname, COUNT(t.id) AS tasks_count
FROM users u
LEFT JOIN tasks t ON t.user_id = u.id
GROUP BY u.id, u.fullname
ORDER BY u.id;
