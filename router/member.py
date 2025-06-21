from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from Model.memeber_Model import MemberDatabase
from Model.s3_model import *

member_router = APIRouter()

member = MemberDatabase()


class SignupForm(BaseModel):
    name: str
    email: str
    password: str


class LoginForm(BaseModel):
    email: str
    password: str


class UpdateForm(BaseModel):
    name: str
    password: str


@member_router.post("/api/user/signup")
async def signup(user: SignupForm):
    try:
        existing_user = member.get_user_by_email(user)
        if existing_user is not None:
            return JSONResponse(status_code=400, content={"success": False, "message": "信箱已註冊，請使用其他信箱。"})
        if existing_user is False:
            return JSONResponse(status_code=500, content={"success": False, "message": "伺服器發生錯誤。"})
        result = member.create_memberdata(user)
        if result is False:
            return JSONResponse(status_code=500, content={"success": False, "message": "帳號創造失敗，請再嘗試一次。"})
        return JSONResponse(status_code=200, content={"success": True})
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(status_code=500, content={"success": False, "message": str(error)})


@member_router.post("/api/user/login")
async def login(user: LoginForm):
    try:
        member_data = member.get_user_data(user)
        if member_data is False:
            return JSONResponse(status_code=500, content={"success": False, "message": "伺服器發生錯誤。"})
        if member_data is None:
            return JSONResponse(status_code=400, content={"success": False, "message": "帳號或密碼錯誤，請重新登入。"})
        token = member.create_JWT(member_data)
        return JSONResponse(status_code=200, content={"success": True, "memberdata": token})
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(status_code=500, content={"success": False, "message": "伺服器發生錯誤。"})


@member_router.patch("/api/user/profile")
async def revise(user: UpdateForm, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"success": False, "message": "未提供有效的授權憑證"})
    token = authorization.split("Bearer ")[1]
    jwt_data = member.check_user_status(token)
    id = jwt_data['id']
    email = jwt_data['email']
    try:
        result = member.update_user_data(id, email, user)
        if result is False:
            return JSONResponse(status_code=500, content={"success": False, "message": "修改資料發生錯誤"})
        return JSONResponse(status_code=200, content={"success": True, "data": result})
    except Exception as error:
        print(f"member_router_Error:{error}")
        return JSONResponse(status_code=500, content={"success": False, "message": "修改資料發生錯誤"})


@member_router.get("/api/user/profile")
async def check_status(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"success": False, "message": "未提供有效的授權憑證"})
    token = authorization.split('Bearer')[1].strip()
    member_data = member.check_user_status(token)
    if member_data is None:
        return JSONResponse(status_code=401, content={"success": False, "message": "未登入系統，拒絕存取"})
    img = member.get_img(member_data['id'])
    if img is False:
        return JSONResponse(status_code=500, content={"success": False, "message": "發生錯誤"})
    member_data['img'] = img['img'] if img else None
    return JSONResponse(status_code=200, content={"success": True, "data": member_data})


@member_router.post("/api/user/uploads")
async def upload_image(file: UploadFile = File(...), authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"success": False, "message": "未提供有效的授權憑證"})
    try:
        token = authorization.split("Bearer ")[1]
        member_data = member.check_user_status(token)
        if member_data is None:
            return JSONResponse(status_code=401, content={"success": False, "message": "未登入系統，拒絕存取"})
        id = member_data['id']
        result = member.get_img(id)
        if result is False:
            return JSONResponse(status_code=500, content={"success": False, "message": "發生錯誤"})
        previous_url = result['img'] if result else None
        url = upload_files_to_S3(file, previous_url)
        if url is False:
            return JSONResponse(status_code=500, content={"error": True, "message": "上傳失敗!"})
        result = member.update_img_url(id, url)
        if result is True:
            return JSONResponse(status_code=200, content={"ok": result})
        if result is False:
            return JSONResponse(status_code=500, content={"error": True, "message": "發生錯誤!"})
        return JSONResponse(status_code=200, content={"ok": True})
    except Exception as error:
        print(f"upload_image error: {error}")
        return JSONResponse(status_code=500, content={"success": False, "message": "伺服器發生錯誤"})
