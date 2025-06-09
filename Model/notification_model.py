from mysql.connector import pooling
import os
from dotenv import load_dotenv


load_dotenv()


class NotificationDatabase:
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

    def get_notification(self, id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = """
                SELECT Notification.*, allbooks.name, allbooks.price, allbooks.img
                FROM notification 
                LEFT JOIN allbooks 
                ON notification.book_id = allbooks.id 
                AND notification.book_source = allbooks.source
                WHERE notification.member_id = %s
            """
            cursor.execute(sql, (id,))
            result = cursor.fetchall()
            print("notification result:", result)
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
