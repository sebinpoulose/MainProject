import mysql.connector

class Database:

    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self, hostname, username, password, database_name):
        self.db = mysql.connector.connect(host=hostname, user=username,passwd=password, database= database_name )
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


