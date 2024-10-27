from sqlalchemy.orm import Session
import models
import schemas


def create_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Notes(title=note.title, description=note.description)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_note_by_id(db: Session, note_id: int):
    return db.query(models.Notes).filter(models.Notes.id == note_id).first()


def get_notes(db: Session):
    return db.query(models.Notes).all()


def get_or_create_tag(db: Session, tag: str):
    db_tag = db.query(models.Tags).filter(models.Tags.name == tag).first()
    if not db_tag:
        db_tag = models.Tags(name=tag)
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
    return db_tag

