from Scrap.scrapscript import BooksRequest, EsliteRequest, SanminRequest
from Scrap.db_model import ScrapDB
from datetime import datetime, timezone, timedelta


def main():

    db = ScrapDB()

    # 每週抓取新書籍資料的流程順序

    eslite = EsliteRequest()
    eslite_new_books = eslite.get_new_books()
    for book in eslite_new_books:
        try:
            db.insert_book_data("eslite", book)
            db.add_daily_price("eslite", book)
        except Exception as e:
            print("誠品新書爬蟲作業錯誤：", e)
            continue

    sanmin = SanminRequest()
    sanmin_new_books = sanmin.get_new_books()
    for book in sanmin_new_books:
        try:
            db.insert_book_data("sanmin", book)
            db.add_daily_price("sanmin", book)
        except Exception as e:
            print("三民新書爬蟲作業錯誤：", e)
            continue

    books = BooksRequest()
    books_new_books = books.get_new_books()
    for book in books_new_books:
        try:
            db.insert_base_data("books", book)
            db.add_daily_price("books", book)
        except Exception as e:
            print("博客來新書爬蟲作業錯誤：", e)
            continue


if __name__ == '__main__':
    main()
