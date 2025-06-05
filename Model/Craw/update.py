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

# eslite_result = []
# eslite_data = db.get_all_id('eslite')
# print("eslite_data:",eslite_data)
# for book in  eslite_data:
#     temp = eslite.get_book_data(book['id'])
#     eslite_result.append(temp)
# for book in eslite_result:
#     db.update_book_data('eslite',book)
#     db.add_daily_price('eslite',book)


# sanmin = SanminRequest()
# sanmin_result = []
# sanmin_data = db.get_all_id('sanmin')
# print("sanmin_data:",sanmin_data)
# for book in sanmin_data:
#     temp = sanmin.get_boook_data(book['id'])
#     sanmin_result.append(temp)
# for book in sanmin_result:
#     db.update_book_data('sanmin',book)
#     db.add_daily_price('sanmin',book)


books = BooksRequest()
books_result = []
books_data = db.get_all_id('books')
print("book_result:", books_result[:3])
count = len(books_data)
for index in range(100, count):
    print(books_data[index]['id'])
    temp = books.get_books_data(books_data[index]['id'])
    books_result.append(temp)
    number = len(books_result)
    if number == 10:
        for book in books_result:
            print("insert")
            db.update_book_data('books', book)
            db.add_daily_price('books', book)
            books_result = []
