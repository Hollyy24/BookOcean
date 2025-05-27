import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv



load_dotenv()

class MemberDatabase:
    def __init__(self):

        dbconfig = {
                    "host":"localhost",
                    "user": os.getenv("MYSQL_USER"),
                    "password": os.getenv("MYSQL_PASSWORD"),
                    "database": "BooksPrice"
                }

        self.cnxpool = pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=5,
                    **dbconfig
                )
    
    def create_memberdata(self,data):
        print("here is create member")
        name = data.name
        email = data.email
        password = self.hash_password(data.password)
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            sql = "INSERT INTO member (name,email,password) VALUE (%s,%s,%s)"
            cursor.execute(sql,(name,email,password,))
            cnx.commit()
            return True
        except Exception as error:
            print(f"錯誤：{error}")
        finally:
            cnx.close()        
    
    def get_memberdata(self,data):
        email = data.email
        password = self.hash_password(data.password)
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "SELECT id ,name  from  member WHERE email = %s  AND password = %s"
            cursor.execute(sql,(email,password,))
            user_data = cursor.fetchone()
            if user_data is None :
                return False 
            return user_data
        except Exception as error:
            print(f"錯誤：{error}")
        finally:
            cnx.close()        
            
    
    # def add_collector_to_book(self,book_id):
    #     cnx = self.cnxpool.get_connection()
    #     cursor = cnx.cursor()
    #     try:
    #         sql = "SELECT id,name  from  member WHERE email =%s  AND password = %s,"
    #         cursor.execute(sql,(email,password,))
    #         user_data = cursor.fetchone()
    #         if len(user_data) == 0 :
    #             return False 
    #         return user_data
    #     except Exception as error:
    #         print(f"錯誤：{error}")
    #     finally:
    #         cnx.close()        
    
    
    def hash_password(self,origin_password):
        return origin_password

    def check_user():
        pass


