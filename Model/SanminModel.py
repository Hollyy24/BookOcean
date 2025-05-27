import requests
from  bs4 import BeautifulSoup
from  selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time,random
from DBModel import DatabaseSystem



class SanminCraw:
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver=webdriver.Chrome(options=options)

    

    #三民書局 搜尋書籍資料
    def sanmin＿search(self,search_name):
        try:
            self.driver.get("https://www.sanmin.com.tw")
            time.sleep(5)
            close_pop = self.driver.find_element(By.XPATH,'//*[@id="PopupAD-close"]')
            close_pop.click()
            time.sleep(1)

            search_input = self.driver.find_element(By.CSS_SELECTOR,'#qu')
            search_input.send_keys(search_name)
            search_input.send_keys(Keys.ENTER)
            
            time.sleep(5)
            
            
            book_list = self.driver.find_elements(By.CSS_SELECTOR,'#Body > div > div > div.col-lg-9.col-12 > div.pl5.pr5 > div.ProductView > div.listview > div.sProduct')
            result = []
            for item in book_list:
                try:
                    book = item.find_element(By.CLASS_NAME,'Title').find_element(By.TAG_NAME,'a')
                    book_url = book.get_attribute('href')
                    book_name = book.text
                    result.append([book_name,book_url])
                except Exception as e:
                    print("e")
                    continue
            return result
        except Exception as e:
            print(e)
            
            
    #三民書局 抓取書籍詳細資料   
    def get_detail_data(self,book_name,book_url):
        try:
            self.driver.get(book_url)
            time.sleep(2)
            intro_content = self.driver.find_elements(By.CLASS_NAME,'mainText')
            book_price = self.driver.find_element(By.CLASS_NAME,'Price').find_element(By.CLASS_NAME,'nowrap').text
            book_img = self.driver.find_element(By.CLASS_NAME,'ProductCover').find_element(By.TAG_NAME,'img').get_attribute('src')
            for item in intro_content:
                if "作者" in item.text:
                    book_author = item.text.split("：")[1]
                if "ISBN" in item.text:
                    book_ISBN = item.text.split("：")[1]
                if "出版社" in item.text:
                    book_publisher =  item.text.split("：")[1]
                if "出版日" in item.text:
                    publisher_date = item.text.split("：")[1]
            time.sleep(1) 
            result ={
                    "來源":"sanmin",
                    "書名":book_name,
                    "ISBN":book_ISBN,
                    "圖片":book_img,
                    "作者":book_author,
                    "價格":book_price,
                    "網站":book_url,
                    "出版商":book_publisher,
                    "出版日":publisher_date
                }
            print(result)
            return result
        except Exception as e:
            print(f'錯誤{e}')
            




    # 從 誠品搜尋 抓書籍資料
    # def fetch_from_eslite(self,search_name):
        URL = f"https://www.eslite.com/Search?keyword={search_name}"
        time.sleep(3)
        try:
            self.driver.get(URL)
            base_data = self.get_eslite_base_data(self)
            return base_data 
        except Exception as e:
            print(f'錯誤：{e}')
        finally:
            self.driver.close()

