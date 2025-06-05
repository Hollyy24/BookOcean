from mysql.connector import pooling
import datetime
import os
from dotenv import load_dotenv


load_dotenv()


class DatabaseSystem:
    def __init__(self):
        dbconfig = {
            "host": os.getenv("MYSQL_HOST"),
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

    def get_all_books(self):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = """
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

    def get_data_by_name(self, name, page):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = """
                WITH merged AS (
                    SELECT id, name, price, isbn, source
                    FROM (
                        SELECT id, name, price, isbn, '博客來' AS source FROM books
                        UNION ALL
                        SELECT id, name, price, isbn, '誠品' AS source FROM eslite
                        UNION ALL
                        SELECT id, name, price, isbn, '三民' AS source FROM sanmin
                    ) AS allbooks
                ),
                isbn_grouped AS (
                    SELECT *, RANK() OVER (ORDER BY isbn) AS isbn_rank
                    FROM merged
                )
                SELECT id, name, price, isbn, source
                FROM isbn_grouped
                WHERE isbn_rank BETWEEN 1 AND 2
                ORDER BY isbn, source;
            """
            name = f'%{name}%'
            # cursor.execute(sql, (name, page,))
            cursor.execute(sql,)
            result = cursor.fetchall()
            print("resutl:", result)
            return result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()

    def get_data_by_author(self, author, page):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = """
                (SELECT id,name,author,price,img,url,'博客來' AS source FROM books WHERE author LIKE %sLIMIT 4 OFFSET %s)
                UNION ALL
                (SELECT id,name,author,price,img,url,'誠品' AS source FROM eslite WHERE author LIKE %sLIMIT 4 OFFSET %s)
                UNION ALL
                (SELECT id,name,author,price,img,url,'三民' AS source FROM sanmin WHERE author LIKE %sLIMIT 4 OFFSET %s)
                """
            author = f'%{author}%'
            cursor.execute(sql, (author, page, author, page, author, page,))
            result = cursor.fetchall()
            return result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()

    def get_similar(self, data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = """
                SELECT *
                FROM
                (SELECT id,name,author,price,img,isbn,url,'博客來' AS source FROM books
                UNION ALL
                SELECT id,name,author,price,img,isbn,url,'誠品' AS source FROM eslite
                UNION ALL
                SELECT id,name,author,price,img,isbn,url,'三民' AS source FROM sanmin )
                AS ALLBOOKS
                WHERE isbn = %s or name LIKE %s or author LIKE %s 
                LIMIT 5
                """
            cursor.execute(
                sql, (data['ISBN'], f"%{data['name']}%", f"%{data['author']}%",))
            result = cursor.fetchall()
            if len(result) == 0:
                return None
            return result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()

    def add_collect_book(self, user_id, data):
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
            cursor.execute(sql, (member_id, book_id, book_source, time,))
            cnx.commit()
            return True
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()

    def get_collect_book(self, member_id):
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
            cursor.execute(sql, (member_id,))
            data = cursor.fetchall()
            if data is None:
                return False
            return data
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()

    def delete_collect_book(self, member_id, data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            book_id = data.book_id
            book_source = data.book_source
            sql = "DELETE FROM collection WHERE member_id=%s AND book_id = %s AND book_source = %s"
            cursor.execute(sql, (member_id, book_id, book_source,))
            cnx.commit()
            return True
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()

    def get_book_detail(self, source, id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            if source == "博客來":
                sql = "SELECT * FROM  books WHERE  id  = %s"
            elif source == "誠品":
                sql = "SELECT * FROM  eslite WHERE  id = %s"
            elif source == "三民":
                sql = "SELECT * FROM  sanmin WHERE  id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            return result
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()

    def get_price_flow(self, source, id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            if source == "博客來":
                sql = "SELECT * FROM  books_price_history WHERE  book_id  =%s"
            elif source == "誠品":
                sql = "SELECT * FROM  eslite_price_history WHERE book_id =%s"
            elif source == "三民":
                sql = "SELECT * FROM  sanmin_price_history WHERE book_id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchall()
            return result
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()
