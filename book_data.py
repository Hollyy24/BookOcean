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
            print("====")

            source = data["來源"]
            name = data["書名"]
            author = data["作者"]
            price = data["價格"]
            img_url = data["圖片"]
            book_url = data["連結"]
            time = datetime.datetime.now().strftime("%Y-%m-%d")
            sql = "INSERT INTO books (source,book_name,book_author,book_price,search_time,book_img_url,book_url) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(source,name,author,price,time,img_url,book_url))
            cnx.commit()
    
        except Exception as error:
            print(f'錯誤:{error}')
        finally:
            cnx.close()
    
    
    def search_data_from_books(self,book_name):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "SELECT id,source,book_name,book_author,book_price,book_img_url,book_url FROM  books WHERE book_name REGEXP %s"
            cursor.execute(sql,(book_name,))
            result = cursor.fetchall()
            return [True,result]
        except Exception as error:
            print(f'error:{error}')
            return [False,error]
        finally:
            cnx.close()
    
    def add_collect_book(self,data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            user_id = data.user_id
            book_id = data.book_id
            sql = "INSERT INTO user_collect_book (user_id,book_id) VALUES (%s,%s)"
            cursor.execute(sql,(user_id,book_id,))
            cnx.commit()
            return True
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()
    
    def get_collect_book(self,user_id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "SELECT id,book_name,book_author,book_price,book_img_url,book_url FROM books WHERE id IN (SELECT book_id FROM user_collect_book WHERE user_id = %s)"
            cursor.execute(sql,(user_id,))
            data = cursor.fetchall()
            if data is None:
                return False 
            return data
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()
    