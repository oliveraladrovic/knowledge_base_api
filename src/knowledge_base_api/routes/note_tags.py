from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from ..schemas import NoteTagIn, NoteTagOut
from ..services import Services, get_service
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=NoteTagOut, status_code=status.HTTP_201_CREATED)
def create_note_tag(
    note_tag: NoteTagIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.create_note_tag(note_tag.model_dump(), db)


@router.get("/", response_model=list[NoteTagOut])
def read_note_tags(
    service: Services = Depends(get_service), db: Session = Depends(get_db)
):
    return service.read_note_tags(db)


@router.put("/{note_tag_id}", response_model=NoteTagOut)
def update_note_tag(
    note_tag_id: int,
    note_tag: NoteTagIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.update_note_tag(note_tag_id, note_tag.model_dump(), db)


@router.delete("/{note_tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_tag(
    note_tag_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    service.delete_note_tag(note_tag_id, db)
