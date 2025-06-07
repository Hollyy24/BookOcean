import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random


class BooksCraw:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)

    # 博客來排行榜 抓書名、網址

    def fetch_books_rank(self):
        result = []
        for i in range(2, 21):
            index = f"{i:02d}"
            url = f"https://www.books.com.tw/web/sys_saletopb/books/{index}/"
            print(url)
            self.driver.get(url)
            time.sleep(5)
            for j in range(1, 101):
                try:
                    book = self.driver.find_element(
                        By.CSS_SELECTOR, f"body > div.container_24.main_wrap.clearfix > div > div:nth-child(2) > div.grid_20.push_4.main_column.alpha > div > div.mod_a.clearfix > ul > li:nth-child({j})")
                    book_name = book.find_element(By.TAG_NAME, 'h4').text
                    content = book.find_element(By.TAG_NAME, 'ul').text
                    print(content.split("\n"))
                    book_author = content.split("\n")[0].replace("作者：", "")
                    book_price = content.split("\n")[1].replace(
                        "優惠價：", "").split("折")[1].replace("元", "")
                    book_url = book.find_element(
                        By.TAG_NAME, 'a').get_attribute("href").split('?')[0]
                    book_img = book.find_element(By.TAG_NAME, 'img').get_attribute(
                        "src").split('http')[2].split("&")[0]
                    temp = {
                        "來源": "books",
                        "書名": book_name,
                        "圖片": "http"+book_img,
                        "作者": book_author,
                        "價格": book_price,
                        "網址": book_url,
                        "id": book_url.replace("https://www.books.com.tw/products/", "")
                    }
                    result.append(temp)
                    print(temp)
                except Exception as e:
                    print(e)
                    continue
        return result


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

    def fetch_books_rank(self):
        result = []
        HEADERS = {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "text/html; charset=UTF-8",
            "Pragma": "no-cache", }
        for i in range(1, 10):
            print(i)
            random_time = random.randint(1, 10)
            print(random_time)
            index = f"{i:02d}"
            URL = f"https://www.books.com.tw/web/sys_saletopb/books/{index}/"
            response = requests.get(url=URL, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')
            book_containers = soup.find_all("li", class_="item")
            time.sleep(random_time)
            print("user -agent:", HEADERS["User-Agent"], "title:", soup.title)
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
                    print(temp)
                    result.append(temp)
                except:
                    print(Exception)
                    continue
        return result

    def get_books_data(self, id):
        result = []
        HEADERS = {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Referer": "https://www.books.com.tw/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-TW",
            "Connection": "keep-alive"}
        try:
            URL = f"https://www.books.com.tw/products/{id}"
            print("user-agent:", HEADERS["User-Agent"])
            print(URL)
            random_time = random.randint(10, 20)
            print(random_time)
            response = requests.get(url=URL, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')
            time.sleep(random_time)
            print("title:", soup.title.get_text())
            book_containers = soup.find("meta", property="og:description")[
                'content'].split("，")
            for item in book_containers:
                print(item)
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
                "url": URL,
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
