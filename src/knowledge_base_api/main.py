from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .exceptions import InvalidDataError
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
