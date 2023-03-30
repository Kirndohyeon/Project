import mysql.connector


class MyDataBase:
    def __init__(self, *, host, user, password, database):
        self.db = mysql.connector.connect(
            host=host, user=user, password=password, database=database)
        self.cursor = self.db.cursor()

    def __del__(self):
        try:
            self.db.close()
        except NameError:
            pass

    def query(self, cmd):
        self.cursor.execute(cmd)

    def fetch(self):
        return self.cursor.fetchall()
