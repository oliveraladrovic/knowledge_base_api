from sqlalchemy.orm import Session
from .exceptions import InvalidDataError, ResourceNotFoundError
from .models import User, Note


class Services:
    # -------------------------
    # USERS
    # -------------------------
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

    def delete_user(self, user_id: int, db: Session) -> None:
        deleting_user = db.query(User).filter(User.id == user_id).first()
        if deleting_user is None:
            raise ResourceNotFoundError("User not found.")

        db.delete(deleting_user)
        db.commit()

    # -------------------------
    # NOTES
    # -------------------------
    def create_note(self, note: dict, db: Session) -> Note:
        user = db.query(User).filter(User.id == note["user_id"]).first()
        if user is None:
            raise ResourceNotFoundError("User not found.")

        note_text = note["text"].strip()
        if not note_text:
            raise InvalidDataError("Note can not be empty.")

        new_note = Note(user_id=user.id, text=note_text)
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        return new_note

    def read_notes(self, db: Session) -> list[Note]:
        return db.query(Note).all()

    def update_note(self, note_id: int, note: dict, db: Session) -> Note:
        updating_note = db.query(Note).filter(Note.id == note_id).first()
        if updating_note is None:
            raise ResourceNotFoundError("Note not found.")

        user = db.query(User).filter(User.id == note["user_id"]).first()
        if user is None:
            raise ResourceNotFoundError("User not found.")

        note_text = note["text"].strip()
        if not note_text:
            raise InvalidDataError("Note can not be empty.")

        updating_note.user_id = user.id
        updating_note.text = note_text
        db.commit()
        db.refresh(updating_note)
        return updating_note

    def delete_note(self, note_id: int, db: Session) -> None:
        deleting_note = db.query(Note).filter(Note.id == note_id).first()
        if deleting_note is None:
            raise ResourceNotFoundError("Note not found.")

        db.delete(deleting_note)
        db.commit()


service = Services()


def get_service():
    return service
