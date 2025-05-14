import requests
from  bs4 import BeautifulSoup
from  selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime
import re



class Craber:
    
    def __init__(self,SEARCH_LIST,DATA_LIST):
        self.search_list=SEARCH_LIST
        self.data_list =DATA_LIST
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver=webdriver.Chrome(options=options)

    
    def disconnection(self):
        self.driver.quit()
    
    

    # 從 誠品 抓書籍資料
    def get_data_from_elsite(self,search_name):
        self.driver.get( f"https://www.eslite.com/Search?keyword={search_name}")
        time.sleep(3)
        try:
            for i in range(1,10):
                book_name = self.driver.find_element(By.CSS_SELECTOR,f' #app > div > div.search-result.ec-container > div.ec-row > div.ec-col-12.lg\:ec-col-10.px-0 > div > div.search-result-area.lg\:pl-2 > div.search-product-block.ec-row.mx-0.px-0 > div:nth-child({i}) > div > div > div.item-wording-wrap > a > div').text.replace("\n","")
                book_author = self.driver.find_element(By.CSS_SELECTOR,f'#app > div > div.search-result.ec-container > div.ec-row > div.ec-col-12.lg\:ec-col-10.px-0 > div > div.search-result-area.lg\:pl-2 > div.search-product-block.ec-row.mx-0.px-0 > div:nth-child({i}) > div > div > div.item-wording-wrap > div.product-publish.flex.flex-col > div > div.product-author.mr-1').text.replace("\n","")
                book_price = self.driver.find_element(By.CSS_SELECTOR,f'#app > div > div.search-result.ec-container > div.ec-row > div.ec-col-12.lg\:ec-col-10.px-0 > div > div.search-result-area.lg\:pl-2 > div.search-product-block.ec-row.mx-0.px-0 > div:nth-child({i}) > div > div > div.item-control-wrap > div > div.product-price').text.replace("\n","")
                result = {
                        "來源":"誠品線上書店",
                        "書名":book_name,
                        "作者":book_author,
                        "價格":book_price
                    }
                print(f'"書名":{book_name},"作者":{book_author},"價格":{book_price}')
                self.data_list.append(result)
        except Exception as e:
            print(f'錯誤：{e}')
        finally:
            return self.data_list

    # 從 博客來 抓書籍資料
    def get_data_from_books(self,search_name):    
        self.driver.get("https://www.books.com.tw/")
        time.sleep(5)
        try:
            search_input = self.driver.find_element(By.CSS_SELECTOR,'#key')
            search_input.send_keys(search_name)
            search_input.send_keys(Keys.ENTER)
            time.sleep(5)
            book_list = self.driver.find_elements(By.CLASS_NAME,'table-td')
            for i in range(1,21):
                book_data = book_list[i].text.split("\n")
                if len(book_data) > 3:
                    print(f'"書名":{book_data[0]},"作者":{book_data[2]},"價格":{book_data[3]}')
                    self.data_list.append({
                        "來源":"博客來",
                        "書名":book_data[0],
                        "作者":book_data[2],
                        "價格":book_data[3]
                    })
        except Exception as e:
            print(f'錯誤：{e}')
        finally:
            return self.data_list

    
    def get_all_datas(self):
        
        for book in self.search_list:
            self.data_list.append(self.get_data_from_books(book))
        for book in self.search_list:
            self.data_list.append(self.get_data_from_elsite(book))
        
        return self.data_list


books = ["被討厭的勇氣","日子","你好","我","哈囉"]
data = []

app = Craber(books,data)

result = app.get_all_datas()
app.disconnection()
print(data)
