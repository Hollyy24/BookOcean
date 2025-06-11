from mysql.connector import pooling
from .db_pool import cnxpool
import os
from dotenv import load_dotenv


load_dotenv()


class NotificationDatabase:
    def __init__(self):
        self.cnxpool = cnxpool

    def get_notification(self, id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = """
                SELECT notification.*, allbooks.name, allbooks.price, allbooks.img
                FROM notification 
                LEFT JOIN allbooks 
                ON notification.book_id = allbooks.id 
                AND notification.book_source = allbooks.source
                WHERE notification.member_id = %s
            """
            cursor.execute(sql, (id,))
            result = cursor.fetchall()
            if len(result) == 0:
                return None
            return result
        except Exception as error:
            print(f"錯誤：{error}")
            return False
        finally:
            cnx.close()

    def update_notification(self, id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "UPDATE notification SET is_read= %s WHERE  id = %s "
            cursor.execute(sql, (True, id,))
            cnx.commit()
            return True
        except Exception as error:
            print(f"錯誤：{error}")
            return False
        finally:
            cnx.close()
