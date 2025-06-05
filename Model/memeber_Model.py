import mysql.connector
from mysql.connector import pooling
import os
import hashlib
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import shutil
import jwt

load_dotenv()
JWT_SECRET = os.getenv("MY_SECRET_KEY")


class MemberDatabase:
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

    def create_memberdata(self, data):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            name = data.name
            email = data.email
            password = self.hash_password(data.password)
            sql = "INSERT INTO member (name,email,password) VALUE (%s,%s,%s)"
            cursor.execute(sql, (name, email, password,))
            cnx.commit()
            return True
        except Exception as error:
            print(f"錯誤：{error}")
            return False
        finally:
            cnx.close()

    def check_memberdata(self, data):
        email = data.email
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "SELECT id ,name  from  member WHERE email = %s "
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
            if result is None:
                return True
            return False
        except Exception as error:
            print(f"錯誤：{error}")
        finally:
            cnx.close()

    def update_memberdata(self, id, email, data):
        name = data.name
        password = self.hash_password(data.password)
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "UPDATE member SET name = %s, password = %s WHERE id = %s "
            cursor.execute(sql, (name, password, id,))
            cnx.commit()
            member = {
                "id": id,
                "name": name,
                "email": email,
            }
            token = self.create_JWT(member)
            return token
        except Exception as error:
            print(f"錯誤：{error}")
            return False
        finally:
            cnx.close()

    def get_memberdata(self, data):
        email = data.email
        password = self.hash_password(data.password)
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "SELECT id ,name,email,img  from  member WHERE email = %s  AND password = %s"
            cursor.execute(sql, (email, password,))
            user_data = cursor.fetchone()
            if user_data is None:
                return False
            return user_data
        except Exception as error:
            print(f"錯誤：{error}")
        finally:
            cnx.close()

    def update_img_url(self, id, url):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "UPDATE member SET img = %s  WHERE id = %s"
            cursor.execute(sql, (url, id))
            cnx.commit()
            return True
        except Exception as error:
            print(f"錯誤：{error}")
            return False
        finally:
            cnx.close()

    def get_img(self, id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "SELECT img  from  member WHERE id= %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            return result
        except Exception as error:
            print(f"錯誤：{error}")
        finally:
            cnx.close()

    def hash_password(self, origin_password):
        temp_password = origin_password.encode()
        hash_password = hashlib.sha256(temp_password).hexdigest()
        return hash_password

    def create_JWT(self, member):
        payload = {
            "id": member["id"],
            "name": member["name"],
            "email": member["email"],
            "exp": (datetime.now(tz=timezone.utc) + timedelta(hours=24*7)).timestamp()
        }
        token = jwt.encode(payload, JWT_SECRET, "HS256")
        return token

    def check_user_status(self, token):
        data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        exp = data.get("exp")
        now = datetime.now(timezone.utc).timestamp()
        if exp and exp < now:
            return None
        elif exp and exp > now:
            result = {
                "id": data["id"],
                "name": data["name"],
                "email": data["email"]
            }
            return result
