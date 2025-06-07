from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from Model.DBModel import DatabaseSystem
from Model.memeber_model import MemberDatabase
import random


book_router = APIRouter()

search = DatabaseSystem()
member = MemberDatabase()


class CollectBook(BaseModel):
    book_source: str
    book_id: str


class BookValue(BaseModel):
    way: str
    value: str
    page: int


class BookDetail(BaseModel):
    source: str
    id: str


@book_router.get("/api/booksdata")
async def getbook():
    try:
        books = search.get_all_books()
        book_count = len(books)-10
        number = []
        for i in range(10):
            number.append(random.randint(0, book_count))
        result = [books[i] for i in number]
        return result
    except Exception as e:
        print("取得所有書籍資料", e)


@book_router.post("/api/booksdata")
async def getData(book: BookValue):
    search = DatabaseSystem()
    try:
        if book.way == "name":
            result = search.get_data_by_name(book.value, book.page)
        elif book.way == "author":
            result = search.get_data_by_author(book.value, book.page)
        if result is False:
            return JSONResponse(content={"success": False, "Message": "資料讀取錯誤"})
        return JSONResponse(content={"success": True, "books": result})
    except Exception as error:
        print(f"藉由書名、作者取得資料錯誤:{error}")
        return JSONResponse(content={"success": False, "Message": error})


@book_router.post("/api/booksdetail")
async def getData(book: BookDetail):
    search = DatabaseSystem()
    try:
        data = search.get_book_detail(book.source, book.id)
        data['publish_date'] = data['publish_date'].isoformat(
        )if data['publish_date'] else None
        data['source'] = book.source
        price_flow = search.get_price_flow(book.source, book.id)
        for item in price_flow:
            item["time"] = item["time"].isoformat() if item['time'] else None
        return JSONResponse(content={"success": True, "data": data, "priceflow": price_flow})
    except Exception as error:
        print(f"取得書本細節錯誤:{error}")
        return JSONResponse(content={"success": False, "Message": "讀取資料錯誤。"})
