from models import Todo
import os
from dotenv import load_dotenv, find_dotenv
import motor.motor_asyncio


load_dotenv(find_dotenv())

DB_CONNECTION_URL = os.environ.get("DB_CONNECTION_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_URL)
database = client.FastAPITaskManager
collection = database.Tasks

async def get_one_todo(id):
    document = await collection.find_one({"id" : id})
    return document

async def get_all_todos():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))

    return todos

async def create_new_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return document

async def update_existing_todo(id, description):
    await collection.update_one({"id" : id}, {"$set" : {
        "description" : description
    }})
    document = await collection.find_one({"id" : id})
    return document

async def delete_existing_todo(id):
    document = await collection.find_one({"id" : id})
    if not document:
        return False
    await collection.delete_one({"id" : id})
    return True

