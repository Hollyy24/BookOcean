from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from Model.book_model import DatabaseSystem
from Model.memeber_Model import MemberDatabase


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
async def get_random_books():
    try:
        result = search.get_all_books()
        print(result)
        if result is False:
            return JSONResponse(status_code=500, content={"success": False, "Message": "資料讀取錯誤"})
        return JSONResponse(status_code=200, content={"success": True, "books": result})
    except Exception as e:
        print("取得所有書籍資料", e)


@book_router.post("/api/booksdata")
async def search_books(book: BookValue):
    search = DatabaseSystem()
    try:
        if book.way == "name":
            result = search.get_data_by_name(book.value, book.page)
        elif book.way == "author":
            result = search.get_data_by_author(book.value, book.page)
        else:
            return JSONResponse(status_code=400, content={"success": False, "Message": "查詢方式錯誤"})
        if result is False:
            return JSONResponse(status_code=500, content={"success": False, "Message": "資料讀取錯誤"})
        return JSONResponse(status_code=200, content={"success": True, "books": result})
    except Exception as error:
        print(f"藉由書名、作者取得資料錯誤:{error}")
        return JSONResponse(status_code=500, content={"success": False, "Message": error})


@book_router.post("/api/booksdetail")
async def get_book_detail(book: BookDetail):
    search = DatabaseSystem()
    try:
        data = search.get_book_detail(book.source, book.id)
        if data is False:
            return JSONResponse(status_code=500, content={"success": False, "Message": "書本資料讀取資料錯誤。"})
        data['source'] = book.source
        price_flow = search.get_price_flow(book.source, book.id)
        if price_flow is False:
            return JSONResponse(status_code=500, content={"success": False, "Message": "歷史價格讀取資料錯誤。"})
        return JSONResponse(status_code=200, content={"success": True, "data": data, "priceflow": price_flow})
    except Exception as error:
        print(f"取得書本路由錯誤:{error}")
        return JSONResponse(status_code=500, content={"success": False, "Message": "讀取資料錯誤。"})
