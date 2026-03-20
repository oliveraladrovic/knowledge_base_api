from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .exceptions import InvalidDataError, ResourceNotFoundError
from .services import Services, get_service
from .schemas import Health, UserIn, UserOut, NoteIn, NoteOut, TagIn, TagOut


app = FastAPI()


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/health", response_model=Health)
def health_check():
    return {"health": "OK"}


# -------------------------
# USERS
# -------------------------
@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    try:
        return service.create_user(user.model_dump(), db)
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))


@app.get("/users", response_model=list[UserOut])
def read_users(service: Services = Depends(get_service), db: Session = Depends(get_db)):
    return service.read_users(db)


@app.get("/users/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    try:
        return service.get_user_by_id(user_id, db)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user: UserIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    try:
        return service.update_user(user_id, user.model_dump(), db)
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    try:
        service.delete_user(user_id, db)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# -------------------------
# NOTES
# -------------------------
@app.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    try:
        return service.create_note(note.model_dump(), db)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))


@app.get("/notes", response_model=list[NoteOut])
def read_notes(service: Services = Depends(get_service), db: Session = Depends(get_db)):
    return service.read_notes(db)


@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note_by_id(
    note_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    try:
        return service.get_note_by_id(note_id, db)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.put("/notes/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    note: NoteIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    try:
        return service.update_note(note_id, note.model_dump(), db)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    try:
        service.delete_note(note_id, db)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get("/users/{user_id}/notes", response_model=list[NoteOut])
def get_notes_by_user_id(
    user_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    try:
        return service.get_notes_by_user_id(user_id, db)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# -------------------------
# TAGS
# -------------------------
@app.post("/tags", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: TagIn, service: Services = Depends(get_service), db: Session = Depends(get_db)
):
    try:
        return service.create_tag(tag.model_dump(), db)
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))
