from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from typing import Union
from starlette.responses import JSONResponse


app = FastAPI(debug=True)

class MessageData(BaseModel):
    assist_api: str
    voice_api: str
    assistant_id: str
    text_for_request: str


@app.get("/")
def read_root():
    return JSONResponse({"message": "Hello, World"})

@app.get('/d')
async def read_docs(): 
    return RedirectResponse(f"/docs")

@app.get('/r')
async def read_redoc(): 
    return RedirectResponse(f"/redoc")

@app.post()
async def add_message(items: MessageData):
    
    return JSONResponse({'message': 'Message hase been added'})



# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

# @app.post("/items/")
# def create_item(item: dict):
#     return item
