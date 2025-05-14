import mysql.connector
from mysql.connector import pooling
import datetime
import os
from dotenv import load_dotenv



load_dotenv()


class BookDatabase:
    def __init__(self):
        dbconfig = {
            "host":"localhost",
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": "BooksPrice"
        }


        self.cnxpool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            **dbconfig
        )


    def insert_book(self,data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            print(data)
            source = data["來源"]
            name = data["書名"]
            author = data["作者"]
            price = data["價格"]
            time = datetime.datetime.now().strftime("%Y-%m-%d")
            if source == "誠品線上書店":
                sql = "INSERT INTO eslite_shop (book_name,book_author,book_price,search_time) VALUES (%s,%s,%s,%s)"
            else:
                sql = "INSERT INTO books_shop (book_name,book_author,book_price,search_time) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql,(name,author,price,time))
            cnx.commit()
    
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()
    
    
    def search_data_from_eslite(self,book_name):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "SELECT book_name,book_author,book_price FROM  eslite_shop  WHERE book_name REGEXP %s"
            cursor.execute(sql,(book_name,))
            result = cursor.fetchall()
            return result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()
    
    def search_data_from_books_shop(self,book_name,):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
    
            sql = "SELECT book_name,book_author,book_price FROM  books_shop  WHERE book_name REGEXP %s"
            cursor.execute(sql,(book_name,))
            result = cursor.fetchall()
            return result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()
            


