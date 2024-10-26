from pydantic import BaseModel
from typing import List, Optional


class Tag(BaseModel):
    name: str


class Note(BaseModel):
    title: str
    description: str
    tags: Optional[List[Tag]] = None
