from mysql.connector import pooling
import datetime
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv


load_dotenv()


dbconfig = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": "BooksPrice"
}


cnxpool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=20,
    **dbconfig
)

try:
    cnx = cnxpool.get_connection()
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
    print(price_result)
except Exception as e:
    print("取得今日歷史價格資料發生錯誤：", e)
finally:
    cnx.close()

if len(price_result) == 0:
    print("返回")


notification = []
for book in price_result:
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        sql = """
        SELECT member_id,book_id,book_source,price FROM collection
        WHERE book_source = %s AND book_id = %s
        """
        cursor.execute(sql, (book['source'], book['book_id'],))
        collection = cursor.fetchone()
        if collection and collection['price'] != book['price']:
            temp = {
                "member_id": collection["member_id"],
                "book_source": collection["book_source"],
                "book_id": collection['book_id'],
                'old_price': collection['price'],
                "new_price": book['price'],
                "is_read": False
            }
            notification.append(temp)
    except Exception as e:
        print("比對收藏資料發生錯誤：", e)
    finally:
        cnx.close()


for book in notification:
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        taiwan_tz = timezone(timedelta(hours=8))
        time = datetime.now(taiwan_tz).strftime("%Y-%m-%d")
        sql = """
        INSERT INTO Notification (member_id,book_id,book_source,old_price,new_price,is_read,time)VALUES
        (%s,%s,%s,%s,%s,%s,%s)
        """
        print(book)
        cursor.execute(sql, (book["member_id"], book["book_id"], book["book_source"],
                       book['old_price'], book["new_price"], book["is_read"], time,))
        cnx.commit()
        print(True)
    except Exception as e:
        print("新增通知資料發生錯誤：", e)
    finally:
        cnx.close()
