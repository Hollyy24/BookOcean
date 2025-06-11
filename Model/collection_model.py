from mysql.connector import pooling
from .db_pool import cnxpool
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()


class CollectionDatabase:

    def __init__(self):
        self.cnxpool = cnxpool

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
