import mysql.connector

# MySQL Connector
class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.connection.cursor()

    def fetch_data(self, query, values):
        self.cursor.execute(query, values)
        results = self.cursor.fetchall()
        return results

    def update_data(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    def insert_data(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_data(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    def execute_query(self, query, values):
        self.cursor.execute(query, values)

    def close(self):
        self.cursor.close()
        self.connection.close()

    def fetchone(self):
        return self.cursor.fetchone()