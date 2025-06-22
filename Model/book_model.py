from mysql.connector import pooling
from .db_pool import cnxpool
from dotenv import load_dotenv
import jieba
import random


class DatabaseSystem:
    def __init__(self):
        self.cnxpool = cnxpool

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
            book_count = len(result)-10
            number = []
            for i in range(10):
                number.append(random.randint(0, book_count))
            random_result = [result[i] for i in number]
            return random_result
        except Exception as error:
            print(f'error:{error}')
        finally:
            cnx.close()

    def get_data_by_name(self, name, page):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = """
                SELECT * FROM allbooks
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
            return False
        finally:
            cnx.close()

    def get_data_by_author(self, author, page):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = """
                SELECT * FROM allbooks WHERE author LIKE %s
                LIMIT 12 OFFSET %s;
            """
            author = f'%{author}%'
            cursor.execute(sql, (author, page,))
            result = cursor.fetchall()
            return result
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
            if result["last_updated"]:
                result["last_updated"] = result["last_updated"].isoformat()[
                    :10]
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
            for item in result:
                item["time"] = item["time"].isoformat() if item['time'] else None
            return result
        except Exception as error:
            print(f'error:{error}')
            return False
        finally:
            cnx.close()
