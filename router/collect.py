from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
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
    book_id: str


@collect_router.post("/api/collect")
async def add_collect_book(authorization: str = Header(None), data: CollectBook = Body(...)):
    token = authorization.split("Bearer ")[1]
    member_id = member.check_user_status(token)['id']
    result = collection.add_collect_book(member_id, data)
    if result is True:
        return JSONResponse(status_code=200, content={"success": True})
    if result is False:
        return JSONResponse(status_code=500, content={"success": False})


@collect_router.delete("/api/collect")
async def delete_collect_book(authorization: str = Header(None), data: CollectBook = Body(...)):
    token = authorization.split("Bearer ")[1]
    member_id = member.check_user_status(token)['id']
    result = collection.delete_collect_book(member_id, data)
    if result is True:
        return JSONResponse(status_code=200, content={"success": True})
    if result is False:
        return JSONResponse(status_code=500, content={"success": False})


@collect_router.get("/api/collect")
async def get_collect_book(authorization: str = Header(None)):
    token = authorization.split("Bearer ")[1]
    member_id = member.check_user_status(token)['id']
    data = collection.get_collect_book(member_id)
    if data:
        return JSONResponse(status_code=200, content={"success": True, "data": data})
    return JSONResponse(status_code=200, content={"success": False})
