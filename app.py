from fastapi import *
from fastapi.responses import FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn


from book_data import BookDatabase
from memeber_data import MemberDatabase

class BookName(BaseModel):
    name :str


class LoginForm(BaseModel):
    name :str
    email:str
    password:str

class SigninForm(BaseModel):
    email:str
    password:str
    
class CollectBook(BaseModel):
    user_id: str
    book_id: str


app=FastAPI()
app.mount("/static",StaticFiles(directory="static"))

member = MemberDatabase()
book = BookDatabase()

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("static/index.html", media_type="text/html")
@app.get("/member", include_in_schema=False)
async def index(request: Request):
	return FileResponse("static/member.html", media_type="text/html")



@app.post("/api/booksdata")
async def getData(book_name:BookName):
    search = BookDatabase()
    try:
        result = search.search_data_from_books(book_name.name)
        if result[0] == False:
            return JSONResponse(content={"success":False,"Message":result[1]})    
        return JSONResponse(content={"success":True,"books":result[1]})    
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(content={"success":False,"Message":error})    
        
    
    
@app.post("/api/loginuser")
async def create_user(user:LoginForm):
    print("login")
    try:
        result = member.create_memberdata(user)
        if result == False:
            return JSONResponse(content={"success":False,"Message":"帳號創造失敗"})    
        return JSONResponse(content={"success":True})    
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(content={"success":False,"Message":str(error)})
    
    
@app.post("/api/signinuser")
async def get_user(user:SigninForm):
    print("signin")
    try:
        result = member.get_memberdata(user)
        print(result)
        if result == False:
            return JSONResponse(content={"success":False,"Message":"登入失敗"})
        return JSONResponse(content={"success":True,"userdata":result})    
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(content={"success":False,"Message":error})  


@app.post("/api/collectbook")
async def add_collect_book(data:CollectBook):
    result = book.add_collect_book(data)
    if result is True:
        return JSONResponse(content={"success":True})
    if result is False:
        return JSONResponse(content={"success":False})
    

@app.get("/api/collectbook")
async def get_collect_book(authorization: str = Header(None)):
    user_id = authorization.replace("Bearer", "")
    data = book.get_collect_book(user_id)
    
    if data :
        return JSONResponse(content={"success":True,"data":data})
    return JSONResponse(content={"success":False})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)