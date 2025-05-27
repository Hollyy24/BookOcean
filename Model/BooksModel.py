import requests
from  bs4 import BeautifulSoup
from  selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time,random
from DBModel import DatabaseSystem




class BooksCraw:
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver=webdriver.Chrome(options=options)

    
    # 博客來排行榜 抓書名、網址
    def fetch_books_rank(self):
        result = []
        for i in range(2,21):
            index = f"{i:02d}"
            url = f"https://www.books.com.tw/web/sys_saletopb/books/{index}/"
            print(url)
            self.driver.get(url)
            time.sleep(5)
            for j in range(1,101):
                try:
                    book = self.driver.find_element(By.CSS_SELECTOR,f"body > div.container_24.main_wrap.clearfix > div > div:nth-child(2) > div.grid_20.push_4.main_column.alpha > div > div.mod_a.clearfix > ul > li:nth-child({j})")
                    book_name = book.find_element(By.TAG_NAME,'h4').text
                    content = book.find_element(By.TAG_NAME,'ul').text
                    print(content.split("\n"))
                    book_author = content.split("\n")[0].replace("作者：","")
                    book_price = content.split("\n")[1].replace("優惠價：","").split("折")[1].replace("元","")
                    book_url = book.find_element(By.TAG_NAME,'a').get_attribute("href").split('?')[0]
                    book_img = book.find_element(By.TAG_NAME,'img').get_attribute("src").split('http')[2].split("&")[0]
                    temp = {
                        "來源":"books",
                        "書名":book_name,
                        "圖片":"http"+book_img,
                        "作者":book_author,
                        "價格":book_price,
                        "網址":book_url,
                        "id":book_url.replace("https://www.books.com.tw/products/","")
                    }
                    result.append(temp)
                    print(temp)
                except Exception as e:
                    print(e)
                    continue
        return result
        
    # #博客來 抓取詳細資料
    # def get_detail_data(self,book_name,book_url,book_id):
    #     try: 
    #         self.driver.get(book_url)
    #         time.sleep(10)
    #         intro =  self.driver.find_element(By.CLASS_NAME,'type02_p003').find_elements(By.TAG_NAME,'li')
    #         for item in intro:
    #             if "作者" in  item.text:
    #                 book_author = item.text.split("\n")[0].split('：')[1]
    #             if "出版社" in  item.text:
    #                 book_publisher = item.text.split("\n")[0].split('：')[1]
    #             if "出版日期" in  item.text:
    #                 publish_date = item.text.split('：')[1]
                    
    #         book_img = self.driver.find_element(By.CLASS_NAME,'cover').get_attribute('src').split("&")[0]
    #         book_price = self.driver.find_element(By.CLASS_NAME,'price01').text
    #         result = {
    #                 "來源":"books",
    #                 "id":book_id,
    #                 "書名":book_name,
    #                 "作者":book_author,
    #                 "圖片":book_img,
    #                 "價格":book_price,
    #                 "網址":book_url,
    #                 "出版社":book_publisher,
    #                 "出版日期":publish_date
    #                 }
    #         print(result)
    #         return result
    #     except Exception as e:
    #         print(e)

    

db = DatabaseSystem()
app = BooksCraw()
books = app.fetch_books_rank()

for book in books:
    db.insert_data(book)