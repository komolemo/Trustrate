import sqlite3

db = sqlite3.connect(
    "../../db.sqlite3", isolation_level=None,
)

create_sql_1 = """
    CREATE TABLE IF NOT EXIST categories (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
    );
"""

create_sql_2 = """
    CREATE TABLE IF NOT EXIST nodes (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    );
"""

create_sql_3 = """
    CREATE TABLE IF NOT EXIST node_relationships (
        parent_id INTEGER,
        child_id INTEGER,
        PRIMARY KEY (parent_id, child_id),
        FOREIGN KEY (parent_id) REFERENCES nodes(id) ON DELETE CASCADE,
        FOREIGN KEY (child_id) REFERENCES nodes(id) ON DELETE CASCADE
    );
"""
db.execute(create_sql_1)
db.execute(create_sql_2)
db.close()