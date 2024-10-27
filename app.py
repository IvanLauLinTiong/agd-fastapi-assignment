from fastapi import FastAPI, HTTPException, Depends, status
from typing import List, Annotated
from sqlalchemy.orm import Session
from database import engine, get_db

import schemas
import models
import crud


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/notes/", response_model=schemas.Note)
async def create_note(note: schemas.NoteCreate, db: db_dependency):
    db_note = crud.create_note(db, note)

    for tag in note.tags:
        db_tag = crud.get_or_create_tag(db, tag)
        db_note.tags.append(db_tag)

    db.commit()
    db.refresh(db_note)
    return db_note


@app.get("/notes/", response_model=List[schemas.Note])
async def get_notes(db: db_dependency):
    db_notes = crud.get_notes(db)
    return db_notes


@app.get("/notes/{note_id}", response_model=schemas.Note)
async def get_note_by_id(note_id: int, db: db_dependency):
    db_note = crud.get_note_by_id(db, note_id)
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return db_note


@app.put("/notes/{note_id}", response_model=schemas.Note)
async def update_note(note_id: int, note: schemas.NoteUpdate,  db: db_dependency):
    # Get exiting note if any
    db_note = crud.get_note_by_id(db, note_id)
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    # Update note
    db_note.title       = note.title
    db_note.description = note.description
    if note.tags:
        db_note.tags = []
        for tag in note.tags:
            db_tag = crud.get_or_create_tag(db, tag)
            db_note.tags.append(db_tag)

    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int, db: db_dependency):
    # Get exiting note if any
    db_note = crud.get_note_by_id(db, note_id)
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}