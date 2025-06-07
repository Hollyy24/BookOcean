
from BooksModel import BooksRequest
from SanminModel import SanminRequest
from EsliteModel import EsliteRequest
from crawDBModel import CrawDB


eslite = EsliteRequest()
db = CrawDB()


# eslite_result = []
# eslite_data = db.get_all_id('eslite')
# print("eslite_data:", eslite_data)
# for book in eslite_data:
#     temp = eslite.get_book_data(book['id'])
#     eslite_result.append(temp)
# for book in eslite_result:
#     db.update_book_data('eslite', book)
#     db.add_daily_price('eslite', book)


# sanmin = SanminRequest()
# sanmin_result = []
# sanmin_data = db.get_all_id('sanmin')
# print("sanmin_data:", sanmin_data)
# for book in sanmin_data:
#     temp = sanmin.get_boook_data(book['id'])
#     sanmin_result.append(temp)
# for book in sanmin_result:
#     db.update_book_data('sanmin', book)
#     db.add_daily_price('sanmin', book)


# books = BooksRequest()
# books_result = []
# books_data = db.get_all_id('books')
# count = len(books_data)
# print(count)
# for index in range(20, 30):
#     print(books_data[index]['id'])
#     temp = books.get_books_data(books_data[index]['id'])
#     books_result.append(temp)
#     number = len(books_result)
#     if number == 10:
#         for book in books_result:
#             print("insert")
#             db.update_book_data('books', book)
#             db.add_daily_price('books', book)
#             books_result = []

sql = "INSERT INTO books_price_history (price, time, book_id) VALUES (%s, %s, %s)"
result = db.get_all_id("books")
for data in result:
    test = {
        "price": "0",
        "id": data["id"],
    }
    db.add_daily_price("books", test)
