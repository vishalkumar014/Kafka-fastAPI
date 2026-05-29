from fastapi import FastAPI,status,Request,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from controller.index import router

app = FastAPI()

@app.middleware('http')
async def middleware(request:Request,next):
    response = await next(request)
    return response

app.include_router(router)



hello

