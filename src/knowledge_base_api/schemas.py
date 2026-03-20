from pydantic import BaseModel, ConfigDict


class Health(BaseModel):
    health: str


class UserIn(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
