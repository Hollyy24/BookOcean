from mysql.connector import pooling
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
import jieba

load_dotenv()


class DatabaseSystem:
    def __init__(self):
        dbconfig = {
            "host": os.getenv("MYSQL_HOST"),
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": "BooksPrice"
        }

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
                SELECT id,name,author,price,img,url,'books' AS source FROM books
                UNION
                SELECT id,name,author,price,img,url,'eslite' AS source FROM eslite
                UNION
                SELECT id,name,author,price,img,url,'sanmin' AS source FROM sanmin
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
                SELECT * FROM Allbooks
                WHERE MATCH(name_fulltext) AGAINST(%s IN BOOLEAN MODE)
                ORDER BY MATCH(name_fulltext) AGAINST(%s IN BOOLEAN MODE) DESC
                LIMIT 12 OFFSET %s;
            """
            words = jieba.cut(name, cut_all=False)
            new_name = " ".join(words)
            cursor.execute(sql, (new_name, new_name, page,))
            result = cursor.fetchall()
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
                SELECT * FROM Allbooks
                WHERE MATCH(author_fulltext) AGAINST(%s IN BOOLEAN MODE)
                ORDER BY MATCH(author_fulltext) AGAINST(%s IN BOOLEAN MODE) DESC
                LIMIT 12 OFFSET %s;
            """
            cursor.execute(sql, (author, author, page,))
            result = cursor.fetchall()
            return result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()

    def add_collect_book(self, user_id, data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            taiwan_tz = timezone(timedelta(hours=8))
            time = datetime.now(taiwan_tz).strftime("%Y-%m-%d")
            member_id = user_id
            book_id = data.book_id
            if data.book_source == "eslite":
                book_source = "eslite"
            elif data.book_source == "books":
                book_source = 'books'
            if data.book_source == "sanmin":
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
            if source == "books":
                sql = "SELECT * FROM books WHERE id = %s"
            elif source == "eslite":
                sql = "SELECT * FROM eslite WHERE id = %s"
            elif source == "sanmin":
                sql = "SELECT * FROM sanmin WHERE id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            return result
        except Exception as error:
            print(f'取得書本細節資料錯誤:{error}')
            return False
        finally:
            cnx.close()

    def get_price_flow(self, source, id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            if source == "books":
                sql = "SELECT * FROM  books_price_history WHERE  book_id  =%s"
            elif source == "eslite":
                sql = "SELECT * FROM  eslite_price_history WHERE book_id =%s"
            elif source == "sanmin":
                sql = "SELECT * FROM  sanmin_price_history WHERE book_id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchall()
            return result
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()
