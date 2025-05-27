from fastapi import *
from fastapi.responses import FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from Model.DBModel import DatabaseSystem
import random



book_router = APIRouter()

search = DatabaseSystem()


    

class CollectBook(BaseModel):
    user_id: str
    book_id: str
    
    
class BookValue(BaseModel):
    way :str
    value:str



@book_router.get("/api/booksdata")
async def getbook():
    print("getall")
    try:
        books = search.get_all_books()
        book_count = len(books)-10
        print(book_count)
        number = [ ]
        for i  in range(10):
            number.append(random.randint(0,book_count))
        result = [books[i] for i in  number]
        print(result)
        return result
    except Exception as e:
        print(e)
    





@book_router.post("/api/booksdata")
async def getData(book:BookValue):
    search =   DatabaseSystem()
    print("get bookdata")
    try:
        if book.way == "name":
            result = search.get_data_by_name(book.value)
            print(f"name:{result}")
        elif book.way == "author":
            result = search.get_data_by_author(book.value)
            print(f"author:{result}")
        if result is  False:
            return JSONResponse(content={"success":False,"Message":"資料讀取錯誤"})    
        return JSONResponse(content={"success":True,"books":result})    
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(content={"success":False,"Message":error})    
        
        

@book_router.delete("/api/collectbook")
async def add_collect_book(data:CollectBook):
    result = search.delete_collect_book(data)
    if result is True:
        return JSONResponse(content={"success":True})
    if result is False:
        return JSONResponse(content={"success":False})


@book_router.post("/api/collectbook")
async def add_collect_book(data:CollectBook):
    result = search.add_collect_book(data)
    if result is True:
        return JSONResponse(content={"success":True})
    if result is False:
        return JSONResponse(content={"success":False})
    

@book_router.get("/api/collectbook")
async def get_collect_book(authorization: str = Header(None)):
    user_id = authorization.replace("Bearer", "")
    data = search.get_collect_book(user_id)
    
    if data :
        return JSONResponse(content={"success":True,"data":data})
    return JSONResponse(content={"success":False})