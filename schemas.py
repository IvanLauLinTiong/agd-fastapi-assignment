from pydantic import BaseModel
from typing import List

# Tag Models
class TagBase(BaseModel):
    name: str

class Tag(TagBase):
    id: int

# Note  Models
class NoteBase(BaseModel):
    title: str
    description: str

class NoteCreate(NoteBase):
    tags: List[str] = []

class NoteUpdate(NoteBase):
    tags: List[str] = []

class NoteWithoutTags(NoteBase):
    id: int

class Note(NoteBase):
    id: int
    tags: List[Tag] = []
