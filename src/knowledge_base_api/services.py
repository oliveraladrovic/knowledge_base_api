from sqlalchemy.orm import Session
from .exceptions import InvalidDataError, ResourceNotFoundError
from .models import User


class Services:
    def create_user(self, user: dict, db: Session) -> User:
        user_name = user["name"].strip()
        if not user_name:
            raise InvalidDataError("Invalid user name.")
        new_user = User(name=user_name)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def read_users(self, db: Session) -> list[User]:
        return db.query(User).all()

    def update_user(self, user_id: int, user: dict, db: Session) -> User:
        updating_user = db.query(User).filter(User.id == user_id).first()
        if updating_user is None:
            raise ResourceNotFoundError("User not found.")
        user_name = user["name"].strip()
        if not user_name:
            raise InvalidDataError("Invalid user name.")
        updating_user.name = user_name
        db.commit()
        db.refresh(updating_user)
        return updating_user


service = Services()


def get_service():
    return service
