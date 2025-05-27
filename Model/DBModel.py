from mysql.connector import pooling
import datetime
import os
from dotenv import load_dotenv



load_dotenv()


class DatabaseSystem:
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

    
    def insert_data(self,data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        print("inseret")
        print(data)
        try:
            book_id = data["id"]
            source = data["來源"]
            name = data["書名"]
            url = data["網址"]
            author= data["作者"]
            img = data["圖片"]
            price = data["價格"]
            if source == "books" :
                sql = "INSERT INTO books (id,name,author,price,URL,img) VALUES (%s,%s,%s,%s,%s,%s)"
            elif source == "eslite":
                sql = "INSERT INTO eslite (id,name,author,price,URL,img) VALUES (%s,%s,%s,%s,%s,%s)"
            elif source == "sanmin":
                sql = "INSERT INTO sanmin (id,name,author,price,URL,img) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(book_id,name,author,price,url,img))
            cnx.commit()
    
        except Exception as error:
            print(f'錯誤:{error}')
        finally:
            cnx.close()
    
    
    def get_all_books(self):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql ="""
                SELECT id,name,author,price,img,url,'博客來' AS source FROM books 
                UNION
                SELECT id,name,author,price,img,url,'誠品' AS source FROM eslite 
                UNION
                SELECT id,name,author,price,img,url,'三民書局' AS source FROM sanmin 
                """
            cursor.execute(sql,)
            result = cursor.fetchall()
            return result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()
    
    
    def get_data_by_name(self,name):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql ="""
                SELECT id,name,author,price,img,url,'博客來' AS source FROM books WHERE name LIKE %s
                UNION
                SELECT id,name,author,price,img,url,'誠品' AS source FROM eslite WHERE name LIKE %s
                UNION
                SELECT id,name,author,price,img,url,'三民書局' AS source FROM sanmin WHERE name LIKE %s
                """
            name  = f'%{name}%'
            cursor.execute(sql,(name,name,name,))
            result = cursor.fetchall()
            return result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()
            
    def get_data_by_author(self,author):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql ="""
                SELECT id,name,author,price,img,url,'博客來' AS source FROM books WHERE author LIKE %s
                UNION
                SELECT id,name,author,price,img,url,'誠品' AS source FROM eslite WHERE author LIKE %s
                UNION
                SELECT id,name,author,price,img,url,'三民書局' AS source FROM sanmin WHERE author LIKE %s
                """
            author  = f'%{author}%'
            cursor.execute(sql,(author,author,author,))
            result = cursor.fetchall()
            return result
        except Exception as error:
            print(f'error:{error}')
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
    
    
    def delete_collect_book(self,user_id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "delete user_collect_book (user_id,book_id) VALUES (%s,%s)"
            cursor.execute(sql,(user_id,))
            cnx.commit()
            return True
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()