from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from ..schemas import TagIn, TagOut, NoteOut
from ..services import Services, get_service
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: TagIn, service: Services = Depends(get_service), db: Session = Depends(get_db)
):
    return service.create_tag(tag.model_dump(), db)


@router.get("/", response_model=list[TagOut])
def read_tags(service: Services = Depends(get_service), db: Session = Depends(get_db)):
    return service.read_tags(db)


@router.put("/{tag_id}", response_model=TagOut)
def update_tag(
    tag_id: int,
    tag: TagIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.update_tag(tag_id, tag.model_dump(), db)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int, service: Services = Depends(get_service), db: Session = Depends(get_db)
):
    service.delete_tag(tag_id, db)


@router.get("/{tag_id}/notes", response_model=list[NoteOut])
def get_notes_by_tag_id(
    tag_id, service: Services = Depends(get_service), db: Session = Depends(get_db)
):
    return service.get_notes_by_tag_id(tag_id, db)
