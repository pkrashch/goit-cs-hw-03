-- create_tables.sql
-- Створення структури бази даних для системи управління завданнями

DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS users;

-- Користувачі
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Статуси завдань
CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Завдання
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER NOT NULL REFERENCES status (id),
    user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE
);

-- Базові статуси
INSERT INTO status (name) VALUES
    ('new'),
    ('in progress'),
    ('completed');
