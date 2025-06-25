import sqlite3

db = sqlite3.connect(
    "db.sqlite3", isolation_level=None,
)

create_categories = """
    CREATE TABLE IF NOT EXISTS training_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        description TEXT
    )
"""

create_trainings = """
    CREATE TABLE IF NOT EXISTS training_programs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL REFERENCES training_category(id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        description TEXT
    );
"""

create_reviews = """
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        training_program_id INTEGER NOT NULL REFERENCES training_program(id) ON DELETE CASCADE,
        user_account_id INTEGER NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,

        overall_rating INTEGER CHECK (overall_rating BETWEEN 1 AND 5),
        contents_rating INTEGER CHECK (contents_rating BETWEEN 1 AND 5),
        lecturer_rating INTEGER CHECK (lecturer_rating BETWEEN 1 AND 5),
        cost_performance_rating INTEGER CHECK (cost_performance_rating BETWEEN 1 AND 5),
        practicality_rating INTEGER CHECK (practicality_rating BETWEEN 1 AND 5),
        ease_of_understanding_rating INTEGER CHECK (ease_of_understanding_rating BETWEEN 1 AND 5),

        comment_summary TEXT,
        pros TEXT,
        cons TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_visible BOOLEAN DEFAULT FALSE
    );
"""

db.execute("""
    DROP TABLE IF EXISTS users;
""")

create_users = """
    CREATE TABLE IF NOT EXISTS  users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(150) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        industory_id INTEGER NOT NULL REFERENCES industories(id) ON DELETE CASCADE,
        password TEXT NOT NULL
    );
"""

create_industories = """
    CREATE TABLE IF NOT EXISTS  industories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );
"""

# sqls = [create_categories, create_trainings, create_reviews, create_users]
sqls = [create_users, create_industories]
for sql in sqls:
    db.execute(sql)

db.close()