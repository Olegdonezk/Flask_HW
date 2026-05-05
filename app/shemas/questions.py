from pydantic import BaseModel
from typing import Optional



class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True



class QuestionCreate(BaseModel):
    text: str
    category_id: int



class QuestionResponse(BaseModel):
    id: int
    text: str
    category: Optional[CategoryBase]

    class Config:
        from_attributes = True