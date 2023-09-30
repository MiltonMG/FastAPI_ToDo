from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Todo, TodoUpdate

router = APIRouter()

#POST: CREAR NUEVO TODO
@router.post("/", response_description="Create a new todo", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def create_todo(request: Request, todo: Todo = Body(...)):
    todo = jsonable_encoder(todo)
    new_todo = request.app.database["todo"].insert_one(todo)
    created_todo = request.app.database["todo"].find_one(
        {"_id": new_todo.inserted_id}
    )

    return created_todo


#GET: OBETENER TODOS LOS TODOS
@router.get("/", response_description="List all Todos", response_model=List[Todo])
async def list_todos(request: Request):
    todos = list(request.app.database["todo"].find(limit=100))
    return todos


#GET BY ID: OBTENER TODO POR ID
@router.get("/{id}", response_description="Get a single todo by id", response_model=Todo)
async def find_todo(id: str, request: Request):
    todo = request.app.database["todo"].find_one({"_id": id})
    if todo is not None:
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {id} not found")


#PUT: ACTUALIZAR TODO BY ID
@router.put("/{id}", response_description="Update a todo", response_model=Todo)
async def update_todo(id: str, request: Request, todo: TodoUpdate = Body(...)):
    todo = {k: v for k, v in todo.model_dump().items() if v is not None}
    if len(todo) >= 1:
        update_result = request.app.database["todo"].update_one(
            {"_id": id}, {"$set": todo}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {id} not found")

    existing_todo = request.app.database["todo"].find_one({"_id": id})
    if existing_todo is not None:
        return existing_todo

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {id} not found")


#DELETE: delete a todo by id
@router.delete("/{id}", response_description="Delete a todo")
async def delete_todo(id: str, request: Request, response: Response):
    delete_result = request.app.database["todo"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {id} not found")



