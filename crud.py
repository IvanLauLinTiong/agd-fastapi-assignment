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


def delete_orphaned_tags(db: Session):
    # Find tags with no associated notes
    orphaned_tags = db.query(models.Tags).filter(~models.Tags.notes.any()).all()
    for tag in orphaned_tags:
        db.delete(tag)
    db.commit()


def get_tags(db: Session):
    return db.query(models.Tags).all()


def get_tag_by_id(db: Session, tag_id: int):
    return db.query(models.Tags).filter(models.Tags.id == tag_id).first()


def get_tag_by_name(db: Session, tag_name: int):
     return db.query(models.Tags).filter(models.Tags.name == tag_name).first()

