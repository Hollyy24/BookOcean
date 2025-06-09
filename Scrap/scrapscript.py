import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random


class BooksRequest():
    def __init__(self):
        self.USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)"
        ]

        self.proxies = {
            "http": "http://123.45.67.89:8080",
            "https": "http://123.45.67.89:8080"
        }

    def fetch_book_rank(self):
        result = []
        HEADERS = {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "text/html; charset=UTF-8",
            "Pragma": "no-cache", }
        for i in range(1, 10):
            random_time = random.randint(1, 10)
            index = f"{i:02d}"
            URL = f"https://www.books.com.tw/web/sys_saletopb/books/{index}/"
            response = requests.get(url=URL, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')
            book_containers = soup.find_all("li", class_="item")
            time.sleep(random_time)
            for i in book_containers:
                try:
                    book_name = i.find("h4").get_text()
                    book_url = i.find("a")['href'].split("?")[0]
                    book_id = book_url.replace(
                        "https://www.books.com.tw/products/", "")
                    temp = {
                        "source": "books",
                        "id": book_id,
                        "name": book_name,
                        "url": book_url
                    }
                    result.append(temp)
                except:
                    print(Exception)
                    continue
        return result

    def get_book_data(self, id, url):
        result = []
        HEADERS = {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Referer": "https://www.books.com.tw/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-TW",
            "Connection": "keep-alive"}
        try:
            random_time = random.randint(10, 20)
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')
            time.sleep(random_time)
            book_containers = soup.find("meta", property="og:description")[
                'content'].split("，")
            for item in book_containers:
                if "作者" in item:
                    book_author = item.split("：")[1]
                elif "ISBN" in item:
                    isbn = item.split("：")[1]
                elif "出版社" in item:
                    book_publisher = item.split("：")[1]
                elif "出版日期" in item:
                    publish_date = item.split("：")[1].replace("/", "-")
            book_name = soup.find('meta', property='og:title')['content']
            book_price = soup.find('meta', property='product:price:amount')[
                'content']
            book_img = soup.find('meta', property='og:image')[
                'content'].split('https://')[2]
            result = {
                "source": "books",
                "name": book_name,
                "author": book_author,
                "id": id,
                "url": url,
                "img": "https://" + book_img.split("&")[0],
                "price": book_price,
                "publisher": book_publisher,
                "publish_date": publish_date,
                "isbn13": isbn if isbn else None
            }
            print(result)
            return result

        except Exception as e:
            print(f"博客來取得書本資料發生錯誤：{e}")


class SanminRequest:

    def __init__(self):
        category = {
            "hi": [f"{i:02d}" for i in range(1, 9)],
            "de": [f"{i:02d}" for i in range(1, 4)],
            "fg": [f"{i:02d}" for i in range(1, 3)],
            "jk": [f"{i:02d}" for i in range(1, 10)],
            "lm": [f"{i:02d}" for i in range(1, 13)],
            "op": [f"{i:02d}" for i in range(1, 9)],
            "qr": [f"{i:02d}" for i in range(1, 3)],
            "st": [f"{i:02d}" for i in range(1, 3)],
            "xy": [f"{i:02d}" for i in range(1, 14)],
        }
        self.category_id = []
        for key, value in category.items():
            for number in value:
                id = f"{key}{number}"
                self.category_id.append(id)

    def get_rank_data(self):
        result = []
        for id in self.category_id:
            for number in range(1, 10):
                try:
                    time.sleep(1)
                    WEB_URL = f'https://www.sanmin.com.tw/promote/library/?id={id}0&pi={number}&groqty=true'
                    response = requests.get(WEB_URL)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    books = soup.find_all('div', class_='sProduct')
                    for book in books:
                        book_name = book.find(
                            'div', class_='Title').find('h3').get_text()
                        book_url = book.find(
                            'div', class_='Title').find('a')['href']
                        book_id = book_url.replace("/product/index/", "")
                        temp = {
                            "source": "sanmin",
                            "id": book_id,
                            "name": book_name,
                            "url": f"https://www.sanmin.com.tw{book_url}",
                        }
                        result.append(temp)
                except Exception as e:
                    print("error:", e)
                    continue
        return result

    def get_childbook_data(self):
        result = []
        for number in range(1, 10):
            for page in range(1, 9):
                try:
                    WEB_URL = f'https://www.sanmin.com.tw/promote/child/?id=ab{number}&pi={page}&groqty=true'
                    response = requests.get(WEB_URL)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    books = soup.find_all('div', class_='sProduct')
                    for book in books:
                        book_name = book.find(
                            'div', class_='Title').find('h3').get_text()
                        book_url = book.find(
                            'div', class_='Title').find('a')['href']
                        book_id = book_url.replace("/product/index/", "")
                        book_data = {
                            "source": "sanmin",
                            "id": book_id,
                            "name": book_name,
                            "url": f"https://www.sanmin.com.tw{book_url}",
                        }
                        result.append(book_data)
                except Exception as e:
                    print(e)
                    continue
        return result

    def get_book_data(self, id):
        try:
            time.sleep(2)
            WEB_URL = f'https://www.sanmin.com.tw/product/index/{id}'
            response = requests.get(WEB_URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            book = soup.find('div', class_='ProductInfo')
            book_name = book.find('h1').get_text()
            into = book.find_all('li', class_='mainText')
            for item in into:
                if "ISBN13" in item.get_text():
                    isbn13 = item.get_text().split("：")[1]
                if "作者" in item.get_text():
                    book_author = item.get_text().split("：")[1]
                if "出版社" in item.get_text():
                    book_publisher = item.get_text().split("：")[1]
                if "出版日" in item.get_text():
                    publish_date = item.get_text().split("：")[
                        1].replace("/", "-")
                if "作者" in item.get_text():
                    book_author = item.get_text().split("：")[1]
            book_price = soup.find('span', class_='Price').get_text()
            book_img = soup.find(
                'div', class_="ProductCover").find('img')['src']
            result = {
                "source": "sanmin",
                "name": book_name,
                "author": book_author,
                "id": id,
                "url": WEB_URL,
                "img": book_img,
                "price": book_price,
                "publisher": book_publisher,
                "publish_date": publish_date,
                "isbn13": isbn13 if isbn13 else None
            }
            print(result)
            return result
        except Exception as e:
            print("error:", e)


class EsliteRequest:

    def get_best_seller(self):
        result = []
        try:
            for i in range(1, 6):
                time.sleep(1)
                url = f'https://athena.eslite.com/api/v1/best_sellers/online/day?l1=3&page={i}&per_page=20'
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
