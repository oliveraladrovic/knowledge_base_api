from fastapi import FastAPI, status, Depends, HTTPException, Request, responses
from sqlalchemy.orm import Session
from .database import get_db
from .exceptions import InvalidDataError, ResourceNotFoundError
from .services import Services, get_service
from .schemas import (
    Health,
    UserIn,
    UserOut,
    NoteIn,
    NoteOut,
    TagIn,
    TagOut,
    NoteTagIn,
    NoteTagOut,
)


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
    return service.create_user(user.model_dump(), db)


@app.get("/users", response_model=list[UserOut])
def read_users(service: Services = Depends(get_service), db: Session = Depends(get_db)):
    return service.read_users(db)


@app.get("/users/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.get_user_by_id(user_id, db)


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user: UserIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.update_user(user_id, user.model_dump(), db)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    service.delete_user(user_id, db)


# -------------------------
# NOTES
# -------------------------
@app.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.create_note(note.model_dump(), db)


@app.get("/notes", response_model=list[NoteOut])
def read_notes(
    tag_name: str = None,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.read_notes(tag_name, db)


@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note_by_id(
    note_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.get_note_by_id(note_id, db)


@app.get("/tags/{tag_id}/notes", response_model=list[NoteOut])
def get_notes_by_tag_id(
    tag_id, service: Services = Depends(get_service), db: Session = Depends(get_db)
):
    return service.get_notes_by_tag_id(tag_id, db)


@app.put("/notes/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    note: NoteIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.update_note(note_id, note.model_dump(), db)


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    service.delete_note(note_id, db)


@app.get("/users/{user_id}/notes", response_model=list[NoteOut])
def get_notes_by_user_id(
    user_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.get_notes_by_user_id(user_id, db)


# -------------------------
# TAGS
# -------------------------
@app.post("/tags", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: TagIn, service: Services = Depends(get_service), db: Session = Depends(get_db)
):
    return service.create_tag(tag.model_dump(), db)


@app.get("/tags", response_model=list[TagOut])
def read_tags(service: Services = Depends(get_service), db: Session = Depends(get_db)):
    return service.read_tags(db)


@app.get("/notes/{note_id}/tags", response_model=list[TagOut])
def get_tags_by_note_id(
    note_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.get_tags_by_note_id(note_id, db)


@app.put("/tags/{tag_id}", response_model=TagOut)
def update_tag(
    tag_id: int,
    tag: TagIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.update_tag(tag_id, tag.model_dump(), db)


@app.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int, service: Services = Depends(get_service), db: Session = Depends(get_db)
):
    service.delete_tag(tag_id, db)


# -------------------------
# NOTE_TAGS
# -------------------------
@app.post("/note_tags", response_model=NoteTagOut, status_code=status.HTTP_201_CREATED)
def create_note_tag(
    note_tag: NoteTagIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.create_note_tag(note_tag.model_dump(), db)


@app.get("/note_tags", response_model=list[NoteTagOut])
def read_note_tags(
    service: Services = Depends(get_service), db: Session = Depends(get_db)
):
    return service.read_note_tags(db)


@app.put("/note_tags/{note_tag_id}", response_model=NoteTagOut)
def update_note_tag(
    note_tag_id: int,
    note_tag: NoteTagIn,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    return service.update_note_tag(note_tag_id, note_tag.model_dump(), db)


@app.delete("/note_tags/{note_tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_tag(
    note_tag_id: int,
    service: Services = Depends(get_service),
    db: Session = Depends(get_db),
):
    service.delete_note_tag(note_tag_id, db)


# -------------------------
# EXCEPTION HANDLING
# -------------------------
@app.exception_handler(ResourceNotFoundError)
def not_found_handler(request: Request, e: ResourceNotFoundError):
    return responses.JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(e), "path": request.url.path, "method": request.method},
    )


@app.exception_handler(InvalidDataError)
def invalid_data_handler(request: Request, e: InvalidDataError):
    return responses.JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(e), "path": request.url.path, "method": request.method},
    )
