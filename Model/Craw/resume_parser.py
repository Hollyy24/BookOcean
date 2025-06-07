import jieba
import os
from mysql.connector import pooling
from dotenv import load_dotenv
import datetime

load_dotenv()
# 連線資料庫
dbconfig = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": "BooksPrice"
}

cnxpool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **dbconfig
)

cnx = cnxpool.get_connection()
cursor = cnx.cursor(dictionary=True)

# 讀取原始內容
cursor.execute("SELECT id,author,source FROM allbooks")
rows = cursor.fetchall()


def char_level_cut(text):
    return " ".join(list(text))


# 斷詞並更新 author_fulltext 欄位
i = 1
for row in rows:
    print(row)
    content = row["author"]
    id = row['id']
    source = row['source']
    content = content or ""
    words = jieba.cut(content, cut_all=False)
    segmented = " ".join(words)
    print(segmented)

    update_sql = "UPDATE allbooks SET author_fulltext = %s WHERE id = %s and source  = %s"
    cursor.execute(update_sql, (segmented, id, source))
    cnx.commit()
    i += 1

cursor.close()
cnx.close()
