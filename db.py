from posix import environ
import psycopg2, os

conn = psycopg2.connect(
    host = os.environ.get("host"),
    database = os.environ.get("database"),
    port = os.environ.get("port"),
    user = os.environ.get("user"),
    password = os.environ.get("password")
)


class DB:
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = psycopg2.connect(dbname)

    def setup(self):
        print("creating table")
        stmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]