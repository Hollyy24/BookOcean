from scrapscript import BooksRequest, EsliteRequest, SanminRequest
from db_model import ScrapDB
from datetime import datetime, timezone, timedelta


def main():

    db = ScrapDB()

    # 每日更新資料的流程順序

    # 1.分別取得 三個書局資料表，離現在日期最遠的15~20本資料（URL,ID) 。
    print("1.分別取得 三個書局資料表，離現在日期最遠的15~20本資料（URL,ID) 。")

    eslite_origin_data = db.get_all_url("eslite")
    books_origin_data = db.get_all_url("books")
    sanmin_origin_data = db.get_all_url("sanmin")

    # 2.先取得這些資料，儲存成 LIST後，更新這些資料(書本資料、價格資料表)。
    print("2.先取得這些資料，儲存成 LIST後，更新這些資料(書本資料、價格資料表)。")

    eslite = EsliteRequest()
    eslite_update_data = []
    print("eslite")
    for book in eslite_origin_data:
        try:
            print(book['id'])
            temp = eslite.get_book_data(book['id'])
            eslite_update_data.append(temp)
        except Exception as e:
            print("誠品取得資料錯誤", e)
            continue
    for book in eslite_update_data:
        try:
            db.update_book_data("eslite", book)
            db.update_allbooks(book['price'], book['id'], "eslite")
            db.add_daily_price("eslite", book)
        except Exception as e:
            print("誠品更新資料錯誤", e)
            continue

    sanmin = SanminRequest()
    sanmin_update_data = []
    print("sanmin")
    for book in sanmin_origin_data:
        try:
            print(book)
            temp = sanmin.get_book_data(book['id'])
            sanmin_update_data.append(temp)
        except Exception as e:
            print("三民取得資料錯誤", e)
            continue
    for book in sanmin_update_data:
        try:
            db.update_book_data("sanmin", book)
            db.update_allbooks(book['price'], book['id'], "sanmin")
            db.add_daily_price("sanmin", book)
        except Exception as e:
            print("三民更新資料錯誤", e)
            continue

    books = BooksRequest()
    books_update_data = []
    print("books")
    for book in books_origin_data:
        try:
            print(book['url'])
            temp = books.get_book_data(book['id'], book['url'])
            books_update_data.append(temp)
        except Exception as e:
            print("博客來更新資料錯誤", e)
            continue
    for book in books_update_data:
        try:
            db.update_book_data("books", book)
            db.update_allbooks(book['price'], book['id'], "books")
            db.add_daily_price("books", book)
        except Exception as e:
            print("博客來更新資料錯誤", e)
            continue
    # 3.刪除離現在超過 180天的書本價格。

    print("3.刪除離現在超過 180天的書本價格。")
    try:
        db.delete_expired_price("books")
        db.delete_expired_price("eslite")
        db.delete_expired_price("sanmin")
    except Exception as e:
        print("刪除過期價格資料錯誤", e)

    # 4.使用 書本來源與書本ID  交叉比對  三個書局的價格資料表(price)  收藏資料表(collection) ，如果有異動就寫進通知資料表

    print("4.使用 書本來源與書本ID  交叉比對  三個書局的價格資料表(price)  收藏資料表(collection) ，如果有異動就寫進通知資料表")

    today_price_list = db.find_today_price()

    notification = []
    for book in today_price_list:
        try:
            temp = db.compare_price_differ(book)
            if temp:
                notification.append(temp)
        except Exception as e:
            print("比較資料或儲存通知發生錯誤", e)
            continue

    for book in notification:
        try:
            db.insert_notification(book)
        except Exception as e:
            print("寫入通知資料發生錯誤", e)
            continue


if __name__ == '__main__':
    main()
