import requests
from bs4 import BeautifulSoup
import time
import random

from BooksModel import BooksRequest
from SanminModel import SanminRequest
from EsliteModel import EsliteRequest
from crawDBModel import CrawDB


db = CrawDB()

eslite = EsliteRequest()
sanmin = SanminRequest()

books_name = db.get_all_name("books")
eslite_name = db.get_all_name('eslite')
sanmin_name = db.get_all_name("sanmin")


temp = books_name + sanmin_name

for name in temp:
    if len(name) > 6:
        name = name[:5]
    print(name)
    result = eslite.search_book(name)
    try:
        for book in result:
            print(book)
            result = db.insert_book_data(book["source"], book)
            print("insert result:", result)
            print("\n\n\n")
            db.add_daily_price(book['source'], book)
    except Exception as e:
        print(f"ESLITE錯誤：{e}")
