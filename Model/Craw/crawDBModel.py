from mysql.connector import pooling
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv


load_dotenv()


class CrawDB:
    def __init__(self):
        dbconfig = {
            "host": os.getenv("MYSQL_HOST"),
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": "BooksPrice"
        }

        self.cnxpool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=20,
            **dbconfig
        )

    def get_all_id(self, source):
        print("get all id")
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            if source == "books":
                sql = "SELECT id,url FROM books "
            elif source == "eslite":
                print("eslite")
                sql = "SELECT id,url FROM eslite "
            elif source == "sanmin":
                print("sanmin")
                sql = "SELECT id,url FROM sanmin "
            else:
                print("none")
            cursor.execute(sql,)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("取得排行榜資料錯誤：", e)
        finally:
            cnx.close()

    def get_all_name(self, source):
        print("get all id")
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            if source == "books":
                print("books")
                sql = "SELECT name FROM books "
            elif source == "eslite":
                print("eslite")
                sql = "SELECT name FROM eslite "
            elif source == "sanmin":
                print("sanmin")
                sql = "SELECT name FROM sanmin "
            else:
                print("none")
                return None
            cursor.execute(sql,)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("取得排行榜資料錯誤：", e)
        finally:
            cnx.close()

    def insert_base_data(self, source, data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        print(source, data)
        try:
            if source == "books":
                sql = "INSERT INTO books (id,name,url) VALUES (%s,%s,%s)"
            if source == "eslite":
                sql = "INSERT INTO eslite (id,name,url) VALUES (%s,%s,%s)"
            if source == "sanmin":
                sql = "INSERT INTO sanmin (id,name,url) VALUES (%s,%s,%s)"
            cursor.execute(sql, (data['id'], data['name'], data['url'],))
            cnx.commit()
        except Exception as e:
            print("儲存資料錯誤：", e)
        finally:
            cnx.close()

    def insert_book_data(self, source, data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        print("insert:", data)
        try:
            if source == "books":
                sql = """
                INSERT INTO books (id,name,author,url,img,price,publisher,publish_date,ISBN)
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            if source == "eslite":
                sql = """
                INSERT INTO eslite (id,name,author,url,img,price,publisher,publish_date,ISBN)
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            if source == "sanmin":
                sql = """
                INSERT INTO sanmin (id,name,author,url,img,price,publisher,publish_date,ISBN)
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            cursor.execute(sql, (data['id'], data['name'], data['author'],
                                 data['url'], data['img'], data['price'],
                                 data['publisher'], data['publish_date'], data['isbn']))
            cnx.commit()
            return True
        except Exception as e:
            print("儲存資料錯誤：", e)
        finally:
            cnx.close()
        cnx.close()

    def update_book_data(self, source, data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        print("update data")
        try:
            if source == "books":
                print('book')
                sql = """
                    UPDATE books
                    SET author = %s,
                        img = %s,
                        publisher = %s,
                        publish_date = %s,
                        url = %s,
                        isbn = %s,
                        price = %s
                        WHERE id = %s
                    """
            if source == "eslite":
                print('eslite')
                sql = """
                    UPDATE eslite
                    SET author = %s,
                        img = %s,
                        publisher = %s,
                        publish_date = %s,
                        url = %s,
                        isbn = %s,
                        price = %s
                        WHERE id = %s
                    """
            if source == "sanmin":
                print('sanmin')

                sql = """
                    UPDATE sanmin
                    SET author = %s,
                        img = %s,
                        publisher = %s,
                        publish_date = %s,
                        url = %s,
                        isbn = %s,
                        price = %s
                        WHERE id = %s
                    """
            cursor.execute(
                sql,
                (data['author'], data['img'], data['publisher'], data['publish_date'], data["url"], data['isbn13'], data['price'], data["id"],))
            cnx.commit()
            return True
        except Exception as e:
            print("更新資料錯誤：", e)
        finally:
            cnx.close()

    def add_daily_price(self, source, data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        taiwan_tz = timezone(timedelta(hours=8))
        now = datetime.now(taiwan_tz).strftime("%Y-%m-%d")
        print("add daily price")
        try:
            if source == "books":
                sql = "INSERT INTO books_price_history (price, time, book_id) VALUES (%s, %s, %s)"
            if source == "eslite":
                sql = "INSERT INTO eslite_price_history (price, time, book_id) VALUES (%s, %s, %s)"
            if source == "sanmin":
                sql = "INSERT INTO sanmin_price_history (price, time, book_id) VALUES (%s, %s, %s)"
            cursor.execute(sql, (data["price"], now, data["id"],))
            cnx.commit()
            return True
        except Exception as e:
            print("新增每日價格失敗：", e)
        finally:
            cnx.close()
