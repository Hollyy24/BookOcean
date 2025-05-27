from fastapi import *
from fastapi.responses import FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from Model.memeber_Model import MemberDatabase




member_router = APIRouter()

member = MemberDatabase()


class LoginForm(BaseModel):
    name :str
    email:str
    password:str
    
    
class SigninForm(BaseModel):
    email:str
    password:str
    
    
@member_router.post("/api/user")
async def login(user:LoginForm):
    print("login")
    try:
        result = member.create_memberdata(user)
        if result == False:
            return JSONResponse(content={"success":False,"Message":"帳號創造失敗"})    
        return JSONResponse(content={"success":True})    
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(content={"success":False,"Message":str(error)})
    
    
@member_router.patch("/api/user")
async def signin(user:SigninForm):
    print("signin")
    try:
        result = member.get_memberdata(user)
        print(result)
        if result == False:
            return JSONResponse(content={"success":False,"Message":"登入失敗"})
        return JSONResponse(content={"success":True,"userdata":result})    
    except Exception as error:
        print(f"Error:{error}")