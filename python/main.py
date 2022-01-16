from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import (
    get_one_todo,
    get_all_todos,
    create_new_todo,
    update_existing_todo,
    delete_existing_todo
)
from models import Todo

app = FastAPI()

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
def home():
    return {"message" : "Hello world"}

@app.get("/api/tasks")
async def get_todos():
    response = await get_all_todos()
    return response


@app.get("/api/tasks/{id}", response_model=Todo)
async def get_todo(id):
    response = await get_one_todo(int(id))
    if response:
        return response
    raise HTTPException(404, "Task not found")

@app.post("/api/tasks/new/create", response_model=Todo)
async def create_todo(todo:Todo):
    response = await create_new_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad request")
    

@app.put("/api/tasks/{id}/update", response_model=Todo)
async def update_todo(id:int, description:str):
    response = await update_existing_todo(int(id), description)
    if response:
        return response

    raise HTTPException(404, "Task does not exist")


@app.delete("/api/tasks/{id}/delete")
async def delete_todo(id):
    response = await delete_existing_todo(int(id))
    if response:
        return {"message" : "Task successfully deleted"}

    raise HTTPException(404, "Task does not exist")