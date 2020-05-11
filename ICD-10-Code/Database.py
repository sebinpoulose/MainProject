import sqlite3


class Database:

    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = sqlite3.connect("./ICD-10-Code/data.sqlite", check_same_thread=False)
        self.cursor = self.db.cursor()

    def insert(self, query, value):
        self.cursor.execute( query, value)
        self.db.commit()
        return self.cursor.rowcount

    def insert_many( self, query, value):
        self.cursor.executemany( query, value)
        self.db.commit()
        return self.cursor.rowcount

    def fetch_data(self, query, value):
        self.cursor.execute( query, value)
        return self.cursor.fetchall()

    def fetch(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, query):
        self.cursor.execute(query)
        self.db.commit()
        return self.cursor.rowcount

    def update_no_commit(self, query):
        self.cursor.execute(query)
        return self.cursor.rowcount

    def commit(self):
        self.db.commit()



