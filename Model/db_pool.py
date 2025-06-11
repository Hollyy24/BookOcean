from mysql.connector import pooling
from dotenv import load_dotenv
import os

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
