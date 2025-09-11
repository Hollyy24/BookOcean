from fastapi import *
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from Model.book_model import DatabaseSystem
from Model.collection_model import CollectionDatabase
from Model.memeber_Model import MemberDatabase


collect_router = APIRouter()

search = DatabaseSystem()
collection = CollectionDatabase()
member = MemberDatabase()


class CollectBook(BaseModel):
    book_source: str
    book_price: str
    book_id: str


@collect_router.get("/api/user/collections")
async def get_user_collected_books(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"success": False, "message": "未提供有效的授權憑證"})
    token = authorization.split("Bearer ")[1]
    token = authorization.split("Bearer ")[1]
    member_id = member.check_user_status(token)['id']
    data = collection.get_collect_book(member_id)
    if data is False:
        return JSONResponse(status_code=500, content={"success": False, "message": "讀取收藏發生錯誤"})
    return JSONResponse(status_code=200, content={"success": True, "data": data})


@collect_router.post("/api/user/collection")
async def add_book_to_collection(authorization: str = Header(None), data: CollectBook = Body(...)):
    print(data)
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"success": False, "message": "未提供有效的授權憑證"})
    token = authorization.split("Bearer ")[1]
    member_id = member.check_user_status(token)['id']
    result = collection.add_collect_book(member_id, data)
    if result is True:
        return JSONResponse(status_code=200, content={"success": True})
    if result is False:
        return JSONResponse(status_code=500, content={"success": False, "message": "新增收藏發生錯誤"})


@collect_router.delete("/api/user/collections/{book_source}/{book_id}")
async def remove_book_from_collection(book_source: str, book_id: str, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"success": False, "message": "未提供有效的授權憑證"})
    token = authorization.split("Bearer ")[1]
    member_id = member.check_user_status(token)['id']
    result = collection.delete_collect_book(member_id, book_id, book_source)
    if result is True:
        return JSONResponse(status_code=200, content={"success": True})
    if result is False:
        return JSONResponse(status_code=500, content={"success": False, "message": "刪除收藏發生錯誤"})
