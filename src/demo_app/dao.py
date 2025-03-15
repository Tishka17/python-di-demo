from sqlite3 import Connection


class UserDAO:
    def __init__(self, connection: Connection):
        self.connection = connection

    def add_user(self, name: str) -> int:
        cursor = self.connection.cursor()
        cursor.execute("insert into users(name) values (?)", (name,))
        return cursor.lastrowid


class LinkDAO:
    def __init__(self, connection: Connection):
        self.connection = connection

    def add_link(self, user_id: int, link: str) -> int:
        cursor = self.connection.cursor()
        cursor.execute("insert into links(user_id, link) values (?, ?)", (user_id, link))
        return cursor.lastrowid


class TransactionManager:
    def __init__(self, connection: Connection):
        self.connection = connection

    def commit(self):
        self.connection.commit()


def create_tables(connection: Connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id primary key,
            name text
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS links(
            id primary key,
            link text,
            user_id integer,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    connection.commit()
