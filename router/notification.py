from fastapi import *
from fastapi.responses import JSONResponse

from Model.memeber_Model import MemberDatabase
from Model.notification_model import NotificationDatabase


notification = NotificationDatabase()
member = MemberDatabase()
notification_router = APIRouter()


@notification_router.get("/api/notification")
async def notify(authorization: str = Header(None)):
    token = authorization.split("Bearer ")[1]
    id = member.check_user_status(token)['id']
    result = notification.get_notification(id)
    if result is False:
        return JSONResponse(status_code=500, content={"success": False, "message": "取得通知發生錯誤"})
    if result is None:
        return JSONResponse(status_code=200, content={"success": True, "data": None})
    return JSONResponse(status_code=200, content={"success": True, "data": result})


@notification_router.put("/api/notification/{notification_id}")
def update_notification(notification_id: int):
    result = notification.update_notification(notification_id)
    if result is False:
        return JSONResponse(status_code=500, content={"success": False, "message": "新增通知發生錯誤"})
    return JSONResponse(status_code=200, content={"success": result})


@notification_router.delete("/api/notification/{notification_id}")
def remove_notification(notification_id: int):
    result = notification.delete_notification(notification_id)
    if result is False:
        return JSONResponse(status_code=500, content={"success": False, "message": "刪除通知發生錯誤"})
    return JSONResponse(status_code=200, content={"success": result})
