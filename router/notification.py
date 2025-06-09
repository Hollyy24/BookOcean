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
        return JSONResponse(status_code=500, content={"success": False, "message": "Internal error"})
    if result is None:
        return JSONResponse(status_code=200, content={"success": True, "data": None})
    for item in result:
        item['time'] = item['time'].isoformat() if item['time'] else None
    return JSONResponse(status_code=200, content={"success": True, "data": result})


@notification_router.put("/api/notification/{notification_id}")
def update_notification(notification_id: int):
    result = notification.update_notification(notification_id)
    return JSONResponse(status_code=200, content={"success": result})
