import sqlite3
from typing import Union, List, Tuple, Any
from pprint import pprint


class Database:
    def __init__(self, db_file: str) -> None:
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str, *args: str) -> List[Tuple]:
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def execute_update(self, query: str,
                       *params: Union[Tuple[Any, ...], None, str]) -> int:
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.rowcount

    def create_table_if_not_exists(self, table_name: str, columns: str) -> None:
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.connection.commit()

    def get_category_name(self, subcategory_name: str, username: str) -> List[Tuple]:
        query = '''
            SELECT c.category_name
            FROM categories c
            JOIN subcategories s ON c.id = s.category_id
            JOIN users u ON u.id = c.user_id
            WHERE s.subcategory_name = ? AND u.username = ?
        '''
        return self.execute_query(query, subcategory_name, username)


db = Database('database.db')







db.create_table_if_not_exists('users', '''
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        token TEXT UNIQUE NOT NULL,
        chat_id TEXT NOT NULL
''')

db.create_table_if_not_exists('categories', '''
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category_name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
''')

db.create_table_if_not_exists('subcategories', '''
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        subcategory_name TEXT NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories (id)
''')

db.create_table_if_not_exists('spot', '''
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        poster_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user (id)
''')
