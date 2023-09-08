import mysql.connector
from PyQt5.QtWidgets import QMessageBox
import os
from dotenv import load_dotenv
load_dotenv()

class Database():   
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = os.getenv('PASSWD')
        self.port = os.getenv('PORT')
        self.database = os.getenv('DB')
        self.con = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            port=self.port,
            database=self.database
        )
        self.c = self.conn.cursor()

    def show_watchList(self):
        try:
            self.connect()
            self.c.execute('select * from watchlist')
            return self.c.fetchall()
    
        except Exception as e:
            print('get data failed')
        finally:
            if self.conn:
                self.conn.close()
            

    def delete_ticker(self, ticker):
        try:
            self.connect()
            self.c.execute(f'delete from watchlist where ticker="{ticker}"')
            self.conn.commit()
        except Exception as e:
            print('could not delete from watchlist')
        finally:
            if self.conn:
                self.conn.close()


    def clear_watchList(self):
        try:
            self.connect()
            self.c.execute('delete from watchlist;')
            self.conn.commit()
        except Exception as e:
            print('could not clear watchlist')
        finally:
            if self.conn:
                self.conn.close()

    def add_ticker(self, symbol, name, exchange):
        try:
            self.connect()
            self.c.execute(f'INSERT into watchlist values(NULL, "{symbol}", "{name}", "{exchange}")')
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()

# -------------------------- LOGIN -------------------------- #

    def get_user_profile(self, email):
        try:
            self.connect()
            self.c.execute(f'SELECT * from users where email="{email}"')
            return self.c.fetchone()
        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()
    
    def insert_user_profile(self, email, password):
        try:
            self.connect()
            self.c.execute(f'INSERT into users values(NULL, "{email}", "{password}")')
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def check_email(self, email):
        try:
            self.connect()
            self.c.execute(f'SELECT * from users where email="{email}"')
            return self.c.fetchone()
        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()