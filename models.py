import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Todo(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    titulo: str = Field(...)
    descripcion: str = Field(...)
    completada: str = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "titulo": "Don Quixote",
                "descripcion": "Miguel de Cervantes",
                "completada": "false"
            }
        }

class TodoUpdate(BaseModel):
    titulo: Optional[str]
    descripcion: Optional[str]
    completada: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Don Quixote",
                "descripcion": "Miguel de Cervantes",
                "completada": "false"
            }
        }