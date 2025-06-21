from mysql.connector import pooling
from Model.db_pool import cnxpool
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv


load_dotenv()


class ScrapDB:
    def __init__(self):
        self.cnxpool = cnxpool

    def get_all_url(self, source):
        print("get all id")
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            if source == "books":
                print("book")
                sql = """
                SELECT id,URL FROM books
                ORDER BY last_updated ASC
                LIMIT 15;"""
            elif source == "eslite":
                print("eslite")
                sql = """
                SELECT id,URL FROM eslite
                ORDER BY last_updated ASC
                LIMIT 20;"""
            elif source == "sanmin":
                print("sanmin")
                sql = """
                SELECT id,URL FROM sanmin
                ORDER BY last_updated ASC
                LIMIT 20;"""
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
                sql = "INSERT INTO books (id,name,URL) VALUES (%s,%s,%s)"
            if source == "eslite":
                sql = "INSERT INTO eslite (id,name,URL) VALUES (%s,%s,%s)"
            if source == "sanmin":
                sql = "INSERT INTO sanmin (id,name,URL) VALUES (%s,%s,%s)"
            cursor.execute(sql, (data['id'], data['name'], data['url'],))
            cnx.commit()
        except Exception as e:
            print("儲存資料錯誤：", e)
        finally:
            cnx.close()

    def insert_book_data(self, source, data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        taiwan_tz = timezone(timedelta(hours=8))
        now = datetime.now(taiwan_tz).strftime("%Y-%m-%d")
        print("insert:", data)
        try:
            if source == "books":
                sql = """
                INSERT INTO books (id,name,author,URL,img,price,publisher,publish_date,ISBN,last_updated)
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            if source == "eslite":
                sql = """
                INSERT INTO eslite (id,name,author,URL,img,price,publisher,publish_date,ISBN,last_updated)
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            if source == "sanmin":
                sql = """
                INSERT INTO sanmin (id,name,author,URL,img,price,publisher,publish_date,ISBN,last_updated)
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            cursor.execute(sql, (data['id'], data['name'], data['author'],
                                 data['url'], data['img'], data['price'],
                                 data['publisher'], data['publish_date'], data['isbn13'], now))
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
        taiwan_tz = timezone(timedelta(hours=8))
        now = datetime.now(taiwan_tz).strftime("%Y-%m-%d")
        try:
            if source == "books":
                sql = """
                    UPDATE books
                    SET author = %s,
                        img = %s,
                        publisher = %s,
                        publish_date = %s,
                        URL = %s,
                        ISBN = %s,
                        price = %s,
                        last_updated = %s
                        WHERE id = %s
                    """
            if source == "eslite":
                sql = """
                    UPDATE eslite
                    SET author = %s,
                        img = %s,
                        publisher = %s,
                        publish_date = %s,
                        URL = %s,
                        ISBN = %s,
                        price = %s,
                        last_updated = %s
                        WHERE id = %s
                    """
            if source == "sanmin":

                sql = """
                    UPDATE sanmin
                    SET author = %s,
                        img = %s,
                        publisher = %s,
                        publish_date = %s,
                        URL = %s,
                        ISBN = %s,
                        price = %s,
                        last_updated = %s
                        WHERE id = %s
                    """
            cursor.execute(
                sql,
                (data['author'], data['img'], data['publisher'],
                 data['publish_date'], data["url"], data['isbn13'],
                 data['price'], now, data["id"],))
            cnx.commit()
            return True
        except Exception as e:
            print("更新資料錯誤：", e)
        finally:
            cnx.close()

    def update_allbooks(self, price, id, source):
        print("update allbooks")
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()

        try:
            sql = """
                UPDATE allbooks
                SET price = %s
                WHERE id = %s AND source = %s
                """
            cursor.execute(sql, (price, id, source,))
            cnx.commit()
            return True
        except Exception as e:
            print("更新 allbooks 資料錯誤：", e)
        finally:
            cnx.close()

    def update_lasted_time(self, source, id):
        print("update last_updated")
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        taiwan_tz = timezone(timedelta(hours=8))
        now = datetime.now(taiwan_tz).strftime("%Y-%m-%d")
        try:
            if source == "books":
                sql = "UPDATE books SET last_updated = %s WHERE id = %s "
            elif source == "eslite":
                sql = "UPDATE eslite SET last_updated = %s WHERE id = %s "
            elif source == "sanmin":
                sql = "UPDATE sanmin SET last_updated = %s WHERE id = %s "
            cursor.execute(sql, (now, id,))
            cnx.commit()
            return True
        except Exception as e:
            print("更新 last_updated 資料錯誤：", e)
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

    def delete_expired_price(self, source):
        print("delete expired price")
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            if source == "books":
                sql = """
                    DELETE FROM books_price_history
                    WHERE time < NOW() - INTERVAL 180 DAY;
                    """
            if source == "eslite":
                sql = """
                    DELETE FROM eslite_price_history
                    WHERE time < NOW() - INTERVAL 180 DAY;
                    """
            if source == "sanmin":
                sql = """
                    DELETE FROM sanmin_price_history
                    WHERE time < NOW() - INTERVAL 180 DAY;
                    """
            cursor.execute(sql)
            cnx.commit()
            return True
        except Exception as e:
            print("刪除過期資料失敗：", e)
        finally:
            cnx.close()

    def find_today_price(self):
        print("find today price")
        try:
            cnx = self.cnxpool.get_connection()
            cursor = cnx.cursor(dictionary=True)
            sql = """
            SELECT source,book_id,price,time FROM (
            SELECT *, 'eslite' as source from eslite_price_history
            UNION ALL
            SELECT *, 'books' as source from books_price_history
            UNION ALL
            SELECT *, 'sanmin' as source from sanmin_price_history)
            AS all_history_price
            WHERE time = %s
            """
            taiwan_tz = timezone(timedelta(hours=8))
            time = datetime.now(taiwan_tz).strftime("%Y-%m-%d")
            cursor.execute(sql, (time,))
            price_result = cursor.fetchall()
            return price_result
        except Exception as e:
            print("取得今日歷史價格資料發生錯誤：", e)
        finally:
            cnx.close()

    def compare_price_differ(self, data):
        try:
            cnx = self.cnxpool.get_connection()
            cursor = cnx.cursor(dictionary=True)
            sql = """
                SELECT member_id,book_id,book_source,price FROM collection
                WHERE book_source = %s AND book_id = %s
                """
            cursor.execute(sql, (data['source'], data['book_id'],))
            collection = cursor.fetchone()
            if collection and collection['price'] != data['price']:
                result = {
                    "member_id": collection["member_id"],
                    "book_source": collection["book_source"],
                    "book_id": collection['book_id'],
                    'old_price': collection['price'],
                    "new_price": data['price'],
                    "is_read": False
                }
                return result
            return None
        except Exception as e:
            print("比對收藏資料發生錯誤：", e)
        finally:
            cnx.close()

    def insert_notification(self, data):
        try:
            cnx = self.cnxpool.get_connection()
            cursor = cnx.cursor(dictionary=True)
            taiwan_tz = timezone(timedelta(hours=8))
            time = datetime.now(taiwan_tz).strftime("%Y-%m-%d")
            sql = """
            INSERT INTO notification 
            (member_id,book_id,book_source,old_price,new_price,is_read,time)
            VALUES
            (%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(sql, (data["member_id"], data["book_id"], data["book_source"],
                                 data['old_price'], data["new_price"], data["is_read"], time,))
            cnx.commit()
            return
        except Exception as e:
            print("新增通知資料發生錯誤：", e)
        finally:
            cnx.close()
