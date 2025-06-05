from fastapi import *
from fastapi.responses import FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn


from router.member import member_router
from router.book import book_router
from router.collect import collect_router


    


app=FastAPI()
app.mount("/static",StaticFiles(directory="static"))
app.include_router(member_router)
app.include_router(book_router)
app.include_router(collect_router)





@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("static/index.html", media_type="text/html")

@app.get("/search/", include_in_schema=False)
async def index(request: Request,way:str,value:str):
	return FileResponse("static/search.html", media_type="text/html")

@app.get("/book", include_in_schema=False)
async def index(request: Request,source:str,id:str):
	return FileResponse("static/book.html", media_type="text/html")

@app.get("/member", include_in_schema=False)
async def index(request: Request):
	return FileResponse("static/member.html", media_type="text/html")







if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)