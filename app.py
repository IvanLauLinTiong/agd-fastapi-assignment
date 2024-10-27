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

    # Clean up orphaned tags
    crud.delete_orphaned_tags(db)

    return db_note

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int, db: db_dependency):
    db_note = crud.get_note_by_id(db, note_id)
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    db.delete(db_note)
    db.commit()

     # Clean up orphaned tags
    crud.delete_orphaned_tags(db)

    return {"message": "Note deleted successfully"}

@app.get("/tags", response_model=List[schemas.Tag])
async def get_tags(db: db_dependency):
    db_tags = crud.get_tags(db)

    return db_tags

@app.get("/tags/{tag_id}/notes", response_model=List[schemas.NoteWithoutTags])
async def get_notes_by_tag_id(tag_id: int, db: db_dependency):
    db_tag = crud.get_tag_by_id(db, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    return db_tag.notes

@app.get("/tags/by-name/{tag_name}/notes", response_model=List[schemas.NoteWithoutTags])
async def get_notes_by_tag_name(tag_name: str, db: db_dependency):
    db_tag = crud.get_tag_by_name(db, tag_name)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    return db_tag.notes