from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from Model.book_model import DatabaseSystem
from Model.memeber_Model import MemberDatabase


book_router = APIRouter()

search = DatabaseSystem()
member = MemberDatabase()


@book_router.get("/api/renderbooks")
async def get_random_books():
    try:
        result = search.get_all_books()
        if result is False:
            return JSONResponse(status_code=500, content={"success": False, "Message": "資料讀取錯誤"})
        return JSONResponse(status_code=200, content={"success": True, "books": result})
    except Exception as e:
        print("取得所有書籍資料", e)


@book_router.get("/api/books")
async def search_books(way: str, value: str, page: int):
    search = DatabaseSystem()
    try:
        if way == "name":
            result = search.get_data_by_name(value, page)
        elif way == "author":
            result = search.get_data_by_author(value, page)
        else:
            return JSONResponse(status_code=400, content={"success": False, "Message": "查詢方式錯誤"})
        if result is False:
            return JSONResponse(status_code=500, content={"success": False, "Message": "資料讀取錯誤"})
        return JSONResponse(status_code=200, content={"success": True, "books": result})
    except Exception as error:
        print(f"藉由書名、作者取得資料錯誤:{error}")
        return JSONResponse(status_code=500, content={"success": False, "Message": error})


@book_router.get("/api/booksdetail")
async def get_book_detail(source: str, id: str):
    search = DatabaseSystem()
    try:
        data = search.get_book_detail(source, id)
        if data is False:
            return JSONResponse(status_code=500, content={"success": False, "Message": "書本資料讀取資料錯誤。"})
        data['source'] = source
        price_flow = search.get_price_flow(source, id)
        if price_flow is False:
            return JSONResponse(status_code=500, content={"success": False, "Message": "歷史價格讀取資料錯誤。"})
        return JSONResponse(status_code=200, content={"success": True, "data": data, "priceflow": price_flow})
    except Exception as error:
        print(f"取得書本路由錯誤:{error}")
        return JSONResponse(status_code=500, content={"success": False, "Message": "讀取資料錯誤。"})
