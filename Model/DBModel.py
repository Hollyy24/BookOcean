from mysql.connector import pooling
import datetime
import os
from dotenv import load_dotenv



load_dotenv()


class DatabaseSystem:
    def __init__(self):
        dbconfig = {
            "host":os.getenv("MYSQL_HOST"),
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": "BooksPrice"
        }
        print(dbconfig["host"])

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
                SELECT id,name,author,price,img,url,'三民' AS source FROM sanmin  
                """
            cursor.execute(sql,)
            result = cursor.fetchall()
            return result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()
    
    
    def get_data_by_name(self,name,page):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql ="""
            (SELECT id,name,author,price,img,url,'博客來' AS source FROM books WHERE name LIKE %s  LIMIT 4 OFFSET %s)
            UNION ALL
            (SELECT id,name,author,price,img,url,'誠品' AS source FROM eslite WHERE name LIKE %s  LIMIT 4 OFFSET %s)
            UNION ALL
            (SELECT id,name,author,price,img,url,'三民' AS source FROM sanmin WHERE name LIKE %s  LIMIT 4 OFFSET %s)
            """
            name  = f'%{name}%'
            cursor.execute(sql,(name,page,name,page,name,page,))
            result = cursor.fetchall()
            print("resutl:",result)
            return result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()
            
    def get_data_by_author(self,author,page):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql ="""
                (SELECT id,name,author,price,img,url,'博客來' AS source FROM books WHERE author LIKE %sLIMIT 4 OFFSET %s)
                UNION ALL
                (SELECT id,name,author,price,img,url,'誠品' AS source FROM eslite WHERE author LIKE %sLIMIT 4 OFFSET %s)
                UNION ALL
                (SELECT id,name,author,price,img,url,'三民' AS source FROM sanmin WHERE author LIKE %sLIMIT 4 OFFSET %s)
                """
            author  = f'%{author}%'
            cursor.execute(sql,(author,page,author,page,author,page,))
            result = cursor.fetchall()
            return result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()
            
    
    
    def add_collect_book(self,user_id,data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            time = datetime.datetime.now().strftime("%Y-%m-%d")
            member_id = user_id
            book_id = data.book_id
            if data.book_source == "誠品":
                book_source = "eslite"
            elif data.book_source == "博客來":
                book_source = 'books'
            if data.book_source == "三民":
                book_source = 'sanmin'
            sql = "INSERT INTO collection (member_id,book_id,book_source,time) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql,(member_id,book_id,book_source,time,))
            cnx.commit()
            return True
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()
    
    
    def get_collect_book(self,member_id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = """
            SELECT
            collection.*,
            allbooks.name,
            allbooks.author,
            allbooks.img,
            allbooks.price,
            allbooks.url
            FROM collection
            LEFT JOIN allbooks
            ON collection.book_id = allbooks.id
            AND collection.book_source = allbooks.source
            WHERE collection.member_id = %s;
            """
            cursor.execute(sql,(member_id,))
            data = cursor.fetchall()
            if data is None:
                return False 
            return data
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()
    
    
    def delete_collect_book(self,member_id,data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            book_id = data.book_id
            book_source = data.book_source
            sql = "DELETE FROM collection WHERE member_id=%s AND book_id = %s AND book_source = %s"
            cursor.execute(sql,(member_id,book_id,book_source,))
            cnx.commit()
            return True
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()