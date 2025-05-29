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
    try:
        no_account = member.check_memberdata(user)
        print(no_account)
        if no_account is False:
            return JSONResponse(content={"success":False,"Message":"信箱已註冊，請使用其他信箱。"})  
        result = member.create_memberdata(user)
        if result == False:
            return JSONResponse(content={"success":False,"Message":"帳號創造失敗，請再嘗試一次。"})    
        return JSONResponse(content={"success":True})    
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(content={"success":False,"Message":str(error)})
    
    
@member_router.patch("/api/user")
async def signin(user:SigninForm):
    try:
        member_data = member.get_memberdata(user)
        print("member_data",member_data)
        if member_data == False:
            return JSONResponse(content={"success":False,"Message":"登入失敗"})
        token = member.create_JWT(member_data)
        print("token:",token)
        return JSONResponse(content={"success":True,"memberdata":token})    
    except Exception as error:
        print(f"Error:{error}")


@member_router.get("/api/user")
async def check_status(authorization: str = Header(None)):
    if not authorization:
        return JSONResponse(content={"success": False, "message": "Missing token"})
    token = authorization.split('Bearer')[1].strip()
    member_data = member.check_user_status(token)
    print("member_data:",member_data)
    if member_data is None:
        return JSONResponse(content={"success":False,"message":"未登入系統，拒絕存取"})
    return JSONResponse(content={"success":True,"data":member_data})
