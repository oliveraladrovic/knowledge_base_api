from pydantic import BaseModel, ConfigDict


class Health(BaseModel):
    health: str


class UserIn(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class NoteIn(BaseModel):
    user_id: int
    text: str


class NoteOut(BaseModel):
    id: int
    user_id: int
    text: str

    model_config = ConfigDict(from_attributes=True)


class TagIn(BaseModel):
    name: str


class TagOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
