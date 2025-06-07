from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from Model.DBModel import DatabaseSystem
from Model.memeber_Model import MemberDatabase


collect_router = APIRouter()

search = DatabaseSystem()
member = MemberDatabase()


class CollectBook(BaseModel):
    book_source: str
    book_id: str


@collect_router.post("/api/collect")
async def add_collect_book(authorization: str = Header(None), data: CollectBook = Body(...)):
    token = authorization.split("Bearer ")[1]
    member_id = member.check_user_status(token)['id']
    result = search.add_collect_book(member_id, data)
    if result is True:
        return JSONResponse(content={"success": True})
    if result is False:
        return JSONResponse(content={"success": False})


@collect_router.delete("/api/collect")
async def delete_collect_book(authorization: str = Header(None), data: CollectBook = Body(...)):
    token = authorization.split("Bearer ")[1]
    member_id = member.check_user_status(token)['id']
    result = search.delete_collect_book(member_id, data)
    if result is True:
        return JSONResponse(content={"success": True})
    if result is False:
        return JSONResponse(content={"success": False})


@collect_router.get("/api/collect")
async def get_collect_book(authorization: str = Header(None)):
    token = authorization.split("Bearer ")[1]
    member_id = member.check_user_status(token)['id']
    data = search.get_collect_book(member_id)
    if data:
        return JSONResponse(content={"success": True, "data": data})
    return JSONResponse(content={"success": False})
