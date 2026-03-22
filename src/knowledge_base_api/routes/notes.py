from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from ..services import Services, get_service
from ..database import get_db
from ..schemas import NoteIn, NoteOut, TagOut

router = APIRouter()


@router.post("/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.create_note(note.model_dump(), db)


@router.get("/", response_model=list[NoteOut])
def read_notes(
    tag_name: str = None,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.read_notes(tag_name, db)


@router.get("/{note_id}", response_model=NoteOut)
def get_note_by_id(
    note_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.get_note_by_id(note_id, db)


@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    note: NoteIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.update_note(note_id, note.model_dump(), db)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    service.delete_note(note_id, db)


@router.get("/{note_id}/tags", response_model=list[TagOut])
def get_tags_by_note_id(
    note_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.get_tags_by_note_id(note_id, db)
