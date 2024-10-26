from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated

from schemas import Note, Tag


app = FastAPI()
