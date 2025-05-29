import requests
from  bs4 import BeautifulSoup
from  selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time,random
from DBModel import DatabaseSystem



class SanminRequest:

    def __init__(self):
        category = {
            "hi":[ f"{i:02d}" for i  in range(1,9)],
            "de":[ f"{i:02d}" for i  in range(1,4)],
            "fg":[ f"{i:02d}" for i  in range(1,3)],
            "jk":[ f"{i:02d}" for i  in range(1,10)],
            "lm":[ f"{i:02d}" for i  in range(1,13)],
            "op":[ f"{i:02d}" for i  in range(1,9)],
            "qr":[ f"{i:02d}" for i  in range(1,3)],
            "st":[ f"{i:02d}" for i  in range(1,3)],
            "xy":[ f"{i:02d}" for i  in range(1,14)],
        }
        self.category_id = [] 
        for key,value in category.items():
            for number in value:
                id = f"{key}{number}"
                self.category_id.append(id)

    def get_rank_data(self):
        result = []
        for id in self.category_id: 
            for number in range(1,10):
                try:
                    time.sleep(1)
                    WEB_URL= f'https://www.sanmin.com.tw/promote/library/?id={id}0&pi={number}&groqty=true'
                    print(WEB_URL)
                    response = requests.get(WEB_URL)
                    soup = BeautifulSoup(response.text,'html.parser')
                    books = soup.find_all('div',class_='sProduct')
                    for book  in books:
                        book_name = book.find('div',class_='Title').find('h3').get_text()
                        book_url = book.find('div',class_='Title').find('a')['href']
                        book_id = book_url.replace("/product/index/","")
                        book_author = book.find('div',class_='Author').find_all('a')[0].get_text()
                        book_price = book.find('span',class_='Price').get_text()
                        book_img = book.find('img')['data-src']
                        book_data  = {
                                "來源":"sanmin",
                                "書名": book_name,
                                "id":book_id,
                                "作者":book_author,
                                "網址": f"https://www.sanmin.com.tw{book_url}",
                                "圖片":book_img,
                                "價格":book_price,
                            }
                        print(book_data)
                        result.append(book_data)
                except Exception as e :
                    print("error:",e)
                    continue    
        return result
            
    def get_childbook_data(self):
        result = []
        for number in range(1,10):
            for page in range(1,9):
                try:
                    print(id)
                    WEB_URL = f'https://www.sanmin.com.tw/promote/child/?id=ab{number}&pi={page}&groqty=true'
                    response = requests.get(WEB_URL)
                    soup = BeautifulSoup(response.text,'html.parser')
                    books = soup.find_all('div',class_='sProduct')
                    for book  in books:
                        book_name = book.find('div',class_='Title').find('h3').get_text()
                        book_url = book.find('div',class_='Title').find('a')['href']
                        book_id = book_url.replace("/product/index/","")
                        book_author = book.find('div',class_='Author').find_all('a')[0].get_text()
                        book_price = book.find('span',class_='Price').get_text()
                        book_img = book.find('img')['data-src']
                        book_data  = {
                                "來源":"sanmin",
                                "書名": book_name,
                                "id":book_id,
                                "作者":book_author,
                                "網址": f"https://www.sanmin.com.tw{book_url}",
                                "圖片":book_img,
                                "價格":book_price,
                            }
                        print(book_data)
                        result.append(book_data)
                except Exception as e :
                    print(e)
                    continue    
        return result
            
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



app = SanminRequest()
db =DatabaseSystem()
books = app.get_rank_data()


for book in books:
    print(book)
    db.insert_data(book)

books = []
books = app.get_childbook_data()
for book in books:
    print(book)
    db.insert_data(book)

