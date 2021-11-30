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
        stmt = "CREATE TABLE IF NOT EXISTS items (description text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, item_text):
        stmt = "INSERT INTO items (description) VALUES (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT description FROM items"
        return [x[0] for x in self.conn.execute(stmt)]