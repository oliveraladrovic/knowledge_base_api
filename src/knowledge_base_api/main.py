from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .exceptions import InvalidDataError, ResourceNotFoundError
from .services import Services, get_service
from .schemas import Health, UserIn, UserOut


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
