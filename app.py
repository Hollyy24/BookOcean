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

app=FastAPI()
app.mount("/static",StaticFiles(directory="static"))

member = MemberDatabase()

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
        if result == False:
            return JSONResponse(content={"success":False,"Message":"登入失敗"})
        return JSONResponse(content={"success":True,"userdata":result})    
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(content={"success":False,"Message":error})  



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)