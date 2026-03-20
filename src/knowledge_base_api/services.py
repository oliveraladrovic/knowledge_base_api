from sqlalchemy.orm import Session
from .exceptions import InvalidDataError
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


service = Services()


def get_service():
    return service
