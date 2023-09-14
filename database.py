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
        self.create_tables

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            port=self.port,
            database=self.database
        )
        self.c = self.conn.cursor()
        

    def create_tables(self):
        try:
            self.connect()
            self.c.execute('''CREATE TABLE IF NOT EXISTS watchlist(
                id INT AUTO_INCREMENT PRIMARY KEY,
                ticker VARCHAR(15) not NULL UNIQUE,
                name VARCHAR(150) not NULL,
                exchange VARCHAR(15)not NULL,
                userID INT,
                FOREIGN KEY (userID) REFERENCES users(id)
            )''')
            
            self.c.execute('''CREATE TABLE IF NOT EXISTS users(
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) not NULL UNIQUE,
                password VARCHAR(300) not NULL,
            )''')

            self.conn.commit()
        except Exception as e:
            print(e)
        
    def show_watchList(self, userid):
        try:
            self.connect()
            self.c.execute(f'select * from watchlist where uid="{userid}"')
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

# -------------------------- POSITION SIZE PAGE -------------------------- #

    def add_position_to_track(self, userid, symbol, entry_price, shares, take_profit, stop_loss):
        try:
            self.connect()
            self.c.execute(f'INSERT into pos_tracker values(NULL, "{userid}", "{symbol}", "{entry_price}", "{shares}", "{take_profit}", "{stop_loss}")')
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def fetch_user_tracks(self, userid):
        try:
            self.connect()
            self.c.execute(f'SELECT * from pos_tracker where user_id="{userid}"')
            return self.c.fetchall()
        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def delete_position_to_track(self, ticker):
        try:
            self.connect()
            self.c.execute(f'delete from pos_tracker where ticker="{ticker}"')
            self.conn.commit()
        except Exception as e:
            print('could not delete from tracker')
        finally:
            if self.conn:
                self.conn.close()

# -------------------------- ALERT PAGE -------------------------- #

    def fetch_users_alerts(self, userid):
        try:
            self.connect()
            self.c.execute(f'select * from alerts where uid="{userid}"')
            return self.c.fetchall()
        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()
    
    def add_alert(self, userid, symbol, type, up_down,  value, email, message):
        try:
            self.connect()
            self.c.execute(f'INSERT into alerts values(NULL, "{userid}", "{symbol}", "{type}", "{up_down}", "{value}", "{email}", "{message}")')
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def delete_alert(self, id, ticker):
        try:
            self.connect()
            self.c.execute(f'delete from alerts where id="{id}" and ticker="{ticker}"')
            self.conn.commit()
        except Exception as e:
            print('could not delete from alerts')
        finally:
            if self.conn:
                self.conn.close()