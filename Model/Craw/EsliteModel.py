
import requests
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class EsliteRequest:

    def get_best_seller(self):
        result = []
        try:
            for i in range(1, 6):
                time.sleep(1)
                url = f'https://athena.eslite.com/api/v1/best_sellers/online/day?l1=3&page={i}&per_page=20'
                print(i)
                response = requests.get(url)
                data = response.json()
                books = data["products"]
                if books is None:
                    return result
                for book in books:
                    book_id = book['id']
                    book_name = book["name"]
                    temp = {
                        "source": "eslite",
                        "name": book_name,
                        "id": book_id,
                        "url": f"https://www.eslite.com/product/{book_id}",
                    }
                    print(temp)
                    result.append(temp)
            return result
        except Exception as e:
            print(f"誠品抓取資料發生錯誤：{e}")
        return result

    def get_book_data(self, id):
        try:
            url = f'https://athena.eslite.com/api/v1/products/{id}'
            response = requests.get(url)
            data = response.json()
            book_name = data['name']
            book_author = data["author"]
            book_price = int(data["retail_price"])
            book_img = data['photos'][0]['small_path']
            isbn13 = data["isbn13"]
            book_publisher = data["supplier"]
            publish_date = data["manufacturer_date"][:10]
            result = {
                "id": id,
                "source": "eslite",
                "name": book_name,
                "author": book_author,
                "url": f"https://www.eslite.com/product/{id}",
                "img": book_img,
                "price": book_price,
                "publisher": book_publisher,
                "publish_date": publish_date,
                "isbn13": isbn13 if isbn13 else None,
            }
            print(result)
            return result
        except Exception as e:
            print(e)

    def get_price(self, id):
        url = f'https://athena.eslite.com/api/v2/products/{id}/prices'
        response = requests.get(url)
        data = response.json()
        price = int(data[0]["retail_price"])
        return price

    def search_book(self, name):
        time.sleep(2)
        result = []
        URL = f"https://athena.eslite.com/api/v2/search?q={name}"
        response = requests.get(URL)
        data = response.json()
        try:
            for book in data["hits"]['hit']:
                book_id = book['id']
                book_info = book['fields']
                book_url = book_info["url"]
                book_name = book_info["name"]
                book_author = book_info["author"][0]
                book_price = book_info["final_price"]
                book_img = "https://s2.eslite.com/unsafe/fit-in/x150/s.eslite.com" + \
                    book_info['product_photo_url']
                isbn = book_info["isbn"]
                book_publisher = book_info["manufacturer"][0]
                publish_date = book_info["manufacturer_date"][:10]
                year = publish_date[6:]
                month = publish_date[0:2]
                day = publish_date[3:5]
                publish_date = year + "-" + month + "-" + day
                temp = {
                    "id": book_id,
                    "source": "eslite",
                    "name": book_name,
                    "author": book_author,
                    "url": book_url,
                    "img": book_img,
                    "price": book_price,
                    "publisher": book_publisher,
                    "publish_date": publish_date,
                    "isbn": isbn if isbn else None,
                }
                result.append(temp)
            return result
        except Exception as e:
            print("誠品搜尋資料錯誤", e)


class EsliteCraw:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)

    # 誠品搜尋資料
    def search_data(self, search_name):
        result = []
        try:
            url = f"https://www.eslite.com/Search?keyword={search_name}"
            self.driver.get(url)
            time.sleep(5)
            book_list = self.driver.find_elements(
                By.CLASS_NAME, 'product-list-wrapper')
            for item in book_list:
                book_name = item.find_element(
                    By.CLASS_NAME, "product-name").text
                book_id = item.find_element(By.CSS_SELECTOR, 'div > a').get_attribute(
                    "href").replace('https://www.eslite.com/product/', "")
                result.append(book_id)
        except Exception as e:
            print(e)
        return result

    # 從誠品排行榜 抓書籍資料

    def fetch_eslite_rank(self):
        result = []
        category_list = [28, 61, 76, 80, 97,
                         23110, 110, 9, 137, 45, 141, 153, 83]
        for category in category_list:
            try:
                time.sleep(5)
                url = f"https://www.eslite.com/best-sellers/online/3/{category}?type=0"
                self.driver.get(url)
                time.sleep(5)
                page_button = self.driver.find_elements(
                    By.CLASS_NAME, 'page-items-group')
                number = len(page_button)
                for _ in range(number):
                    book_list = self.driver.find_elements(
                        By.CLASS_NAME, 'product-list-wrapper')
                    for item in book_list:
                        book_name = item.find_element(
                            By.CLASS_NAME, "product-name").text
                        book_url = item.find_element(
                            By.CSS_SELECTOR, 'div > a').get_attribute("href")
                        temp = {
                            "來源": "eslites",
                            "書名": book_name,
                            "網址": book_url
                        }
                        result.append(temp)
                    time.sleep(2)
                    next_button = self.driver.find_element(
                        By.CSS_SELECTOR, f'#app > div > div.eslite-bookstore.pb-3 > div > div > div.ec-col-12.lg\:ec-col-10.xl\:pl-2.mt-4 > div > div:nth-child(3) > div.search-products-pagination.flex.px-0.pt-6.pb-1 > div > div:nth-child({number+2})')
                    next_button.click()
                    time.sleep(3)
            except Exception as e:
                print(e)
                continue
        return result

    # 誠品 取得書名、網址
    def get_eslite_base_data(self):
        temp = []
        book_list = self.driver.find_elements(
            By.CLASS_NAME, 'product-list-wrapper')
        for item in book_list:
            book_name = item.find_element(
                By.CLASS_NAME, "product-name").text
            book_url = item.find_element(
                By.CSS_SELECTOR, 'div > a').get_attribute("href")
            result = {
                "來源": "eslites",
                "書名": book_name,
                "網址": book_url
            }
            temp.append(result)
        return temp

    # 誠品 抓取書本細節
    def get_eslite_detail_data(self, book_name, book_url, book_id):
        try:
            self.driver.get(book_url)
            time.sleep(5)
            book_author = self.driver.find_element(
                By.CLASS_NAME, 'author').text.replace("\n", "").split("：")[1]
            book_img = self.driver.find_element(
                By.CLASS_NAME, 'swiper-wrapper').find_element(By.TAG_NAME, 'img').get_attribute("src")
            book_price = self.driver.find_element(
                By.CLASS_NAME, 'item-price').text
            book_publisher = self.driver.find_element(
                By.CLASS_NAME, 'publisher').text.replace("\n", "").split("：")[1]
            publish_date = self.driver.find_element(
                By.CLASS_NAME, 'publicDate').text.replace("\n", "").split("：")[1]
            result = {
                "來源": "eslite",
                "id": book_id,
                "書名": book_name,
                "作者": book_author,
                "圖片": book_img,
                "價格": book_price,
                "網址": book_url,
                "出版社": book_publisher,
                "出版日期": publish_date
            }
            print(result)
            return result
        except Exception as e:
            print(e)


app = EsliteRequest()
app.search_book("花婆婆")
