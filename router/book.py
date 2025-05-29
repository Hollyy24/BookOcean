from fastapi import *
from fastapi.responses import FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from Model.DBModel import DatabaseSystem
from Model.memeber_Model import MemberDatabase
import random



book_router = APIRouter()

search = DatabaseSystem()
member = MemberDatabase()

    

class CollectBook(BaseModel):
    book_source: str
    book_id: str
    
    
class BookValue(BaseModel):
    way :str
    value:str



@book_router.get("/api/booksdata")
async def getbook():
    try:
        books = search.get_all_books()
        book_count = len(books)-10
        number = [ ]
        for i  in range(10):
            number.append(random.randint(0,book_count))
        result = [books[i] for i in  number]
        return result
    except Exception as e:
        print(e)
    





@book_router.post("/api/booksdata")
async def getData(book:BookValue):
    search =   DatabaseSystem()
    try:
        if book.way == "name":
            result = search.get_data_by_name(book.value)
        elif book.way == "author":
            result = search.get_data_by_author(book.value)
        if result is  False:
            return JSONResponse(content={"success":False,"Message":"資料讀取錯誤"})    
        return JSONResponse(content={"success":True,"books":result})    
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(content={"success":False,"Message":error})    
        


