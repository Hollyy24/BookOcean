from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from Model.memeber_Model import MemberDatabase
from Model.s3_upload import *

member_router = APIRouter()

member = MemberDatabase()


class LoginForm(BaseModel):
    name: str
    email: str
    password: str


class SigninForm(BaseModel):
    email: str
    password: str


class UpdateForm(BaseModel):
    name: str
    password: str


@member_router.post("/api/userLogin")
async def login(user: LoginForm):
    try:
        no_account = member.check_memberdata(user)
        if no_account is False:
            return JSONResponse(content={"success": False, "Message": "信箱已註冊，請使用其他信箱。"})
        result = member.create_memberdata(user)
        if result == False:
            return JSONResponse(content={"success": False, "Message": "帳號創造失敗，請再嘗試一次。"})
        return JSONResponse(content={"success": True})
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(content={"success": False, "Message": str(error)})


@member_router.post("/api/userSignin")
async def signin(user: SigninForm):

    try:
        member_data = member.get_memberdata(user)
        if member_data == False:
            return JSONResponse(content={"success": False, "Message": "登入失敗"})
        token = member.create_JWT(member_data)
        return JSONResponse(content={"success": True, "memberdata": token})
    except Exception as error:
        print(f"Error:{error}")


@member_router.patch("/api/userSignin")
async def revise(user: UpdateForm, authorization: str = Header(None)):
    token = authorization.split("Bearer ")[1]
    jwt_data = member.check_user_status(token)
    id = jwt_data['id']
    email = jwt_data['email']
    try:
        result = member.update_memberdata(id, email, user)
        if result == False:
            return JSONResponse(content={"success": False, "Message": "失敗"})
        return JSONResponse(content={"success": True, "data": result})
    except Exception as error:
        print(f"member_router_Error:{error}")


@member_router.get("/api/userSignin")
async def check_status(authorization: str = Header(None)):
    if not authorization:
        return JSONResponse(content={"success": False, "message": "Missing token"})
    token = authorization.split('Bearer')[1].strip()
    member_data = member.check_user_status(token)
    img = member.get_img(member_data['id'])
    member_data['img'] = img['img'] if img else None
    if member_data is None:
        return JSONResponse(content={"success": False, "message": "未登入系統，拒絕存取"})
    return JSONResponse(content={"success": True, "data": member_data})


@member_router.post("/api/uploads")
async def upload_image(file: UploadFile = File(...), authorization: str = Header(None)):
    token = authorization.split("Bearer ")[1]
    id = member.check_user_status(token)['id']
    result = member.get_img(id)
    previous_url = result['img'] if result else None
    url = upload_files_to_S3(file, previous_url)
    if url is False:
        return JSONResponse(content={"error": True, "message": "上傳失敗!"})
    result = member.update_img_url(id, url)
    if result is True:
        return JSONResponse(content={"ok": result})
    if result is False:
        return JSONResponse(content={"error": True, "message": "發生錯誤!"})
    return JSONResponse(content={"ok": True})


@member_router.get("/api/notification")
async def notify(authorization: str = Header(None)):
    token = authorization.split("Bearer ")[1]
    id = member.check_user_status(token)['id']
    result = member.get_notification(id)
    for item in result:
        item['time'] = item['time'].isoformat() if item['time'] else None
    if result is False:
        return JSONResponse(content={"success": False})
    return JSONResponse(content={"success": True, "data": result})


@member_router.put("/api/notification/{notification_id}")
def update_notification(notification_id: int):
    result = member.update_notification(notification_id)
    return JSONResponse(content={"success": result})
