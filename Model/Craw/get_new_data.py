from BooksModel import BooksRequest
from SanminModel import SanminRequest
from EsliteModel import EsliteRequest
from crawDBModel import CrawDB


db = CrawDB()
books = BooksRequest()
sanmin = SanminRequest()
eslite = EsliteRequest()


new_data = []
eslite_ranks_result = eslite.get_best_seller()
compare_id = db.get_all_id("eslite")
for item in eslite_ranks_result:
    if item['id'] not in compare_id:
        new_data.append(item)

for book in new_data:
    try:
        db.insert_base_data(book['source'], book)
    except Exception as e:
        print("儲存誠品資料錯誤：", e)
        continue


new_data = []

books_rank_result = books.fetch_books_rank()
compare_id = db.get_all_id("books")
for item in books_rank_result:
    if item['id'] not in compare_id:
        new_data.append(item)
for book in new_data:
    try:
        print(book)
        db.insert_base_data(book['source'], book)
    except Exception as e:
        print("儲存博客來資料錯誤：", e)
        continue


new_data = []
sanmin_rank_result_1 = sanmin.get_rank_data()
sanmin_rank_result_2 = sanmin.get_childbook_data()
sanmin_rank_result = sanmin_rank_result_1 + sanmin_rank_result_2
compare_id = db.get_all_id("sanmin")
for item in sanmin_rank_result:
    if item['id'] not in compare_id:
        new_data.append(item)
for book in new_data:
    try:
        print(book)
        db.insert_base_data(book['source'], book)
    except Exception as e:
        print("儲存三民資料錯誤：", e)
        continue
