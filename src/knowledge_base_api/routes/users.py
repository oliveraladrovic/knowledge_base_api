from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from ..schemas import UserIn, UserOut, NoteOut
from ..services import Services, get_service
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.create_user(user.model_dump(), db)


@router.get("/", response_model=list[UserOut])
def read_users(service: Services = Depends(get_service), db: Session = Depends(get_db)):
    return service.read_users(db)


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.get_user_by_id(user_id, db)


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user: UserIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.update_user(user_id, user.model_dump(), db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    service.delete_user(user_id, db)


@router.get("/{user_id}/notes", response_model=list[NoteOut])
def get_notes_by_user_id(
    user_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.get_notes_by_user_id(user_id, db)
