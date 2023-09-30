from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as todo_router

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient("mongodb+srv://user_node:node@cluster-node.1jvlzyq.mongodb.net")
    app.database = app.mongodb_client["todo"]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(todo_router, tags=["todos"], prefix="/todo")