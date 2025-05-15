from fastapi import *
from fastapi.responses import FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn


from data import BookDatabase

class BookName(BaseModel):
    name :str


app=FastAPI()
app.mount("/static",StaticFiles(directory="static"))


@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("static/index.html", media_type="text/html")


@app.post("/api/booksdata")
async def getData(book_name:BookName):
    search = BookDatabase()
    try:
        result_1 = search.search_data_from_books_shop(book_name.name)
        result_2 = search.search_data_from_eslite(book_name.name)
        result = result_1 + result_2
        return JSONResponse(content={"success":True,"books":result_1,"eslite":result_2})    
    except Exception as error:
        print(f"Error:{error}")
        return JSONResponse(content={"success":False,"Message":error})    
        
    
    
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)