from sqlalchemy.orm import Session
from .exceptions import InvalidDataError, ResourceNotFoundError
from .models import User, Note, Tag, NoteTag


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

    def get_user_by_id(self, user_id: int, db: Session) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ResourceNotFoundError("User not found.")

        return user

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

        invalid_notes = db.query(Note).filter(Note.user_id == user_id).all()
        for note in invalid_notes:
            invalid_note_tags = (
                db.query(NoteTag).filter(NoteTag.note_id == note.id).all()
            )
            for note_tag in invalid_note_tags:
                db.delete(note_tag)
            db.delete(note)

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

    def get_note_by_id(self, note_id: int, db: Session) -> Note:
        note = db.query(Note).filter(Note.id == note_id).first()
        if note is None:
            raise ResourceNotFoundError("Note not found.")

        return note

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

        invalid_note_tags = db.query(NoteTag).filter(NoteTag.note_id == note_id).all()
        for note_tag in invalid_note_tags:
            db.delete(note_tag)

        db.delete(deleting_note)
        db.commit()

    def get_notes_by_user_id(self, user_id: int, db: Session) -> list[Note]:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ResourceNotFoundError("User not found.")

        return user.notes

    # -------------------------
    # TAGS
    # -------------------------
    def create_tag(self, tag: dict, db: Session) -> Tag:
        tag_name = tag["name"].strip().lower()
        if not tag_name:
            raise InvalidDataError("Tag can not be empty.")

        existing = db.query(Tag).filter(Tag.name == tag_name).first()
        if existing is not None:
            raise InvalidDataError("Tag already exist.")

        new_tag = Tag(name=tag_name)
        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)
        return new_tag

    def read_tags(self, db: Session) -> list[Tag]:
        return db.query(Tag).all()

    def update_tag(self, tag_id: int, tag: dict, db: Session) -> Tag:
        updating_tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if updating_tag is None:
            raise ResourceNotFoundError("Tag not found.")

        tag_name = tag["name"].strip().lower()
        if not tag_name:
            raise InvalidDataError("Tag can not be empty.")

        existing = db.query(Tag).filter(Tag.name == tag_name).first()
        if existing is not None:
            raise InvalidDataError("Tag already exists.")

        updating_tag.name = tag_name
        db.commit()
        db.refresh(updating_tag)
        return updating_tag

    def delete_tag(self, tag_id: int, db: Session) -> None:
        deleting_tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if deleting_tag is None:
            raise ResourceNotFoundError("Tag not found.")

        invalid_note_tags = db.query(NoteTag).filter(NoteTag.tag_id == tag_id).all()
        for note_tag in invalid_note_tags:
            db.delete(note_tag)

        db.delete(deleting_tag)
        db.commit()

    # -------------------------
    # NOTES / TAGS
    # -------------------------
    def create_note_tag(self, note_tag: dict, db: Session) -> NoteTag:
        note = db.query(Note).filter(Note.id == note_tag["note_id"]).first()
        if note is None:
            raise ResourceNotFoundError("Note not found.")

        tag = db.query(Tag).filter(Tag.id == note_tag["tag_id"]).first()
        if tag is None:
            raise ResourceNotFoundError("Tag not found.")

        existing = (
            db.query(NoteTag)
            .filter(NoteTag.note_id == note.id, NoteTag.tag_id == tag.id)
            .first()
        )
        if existing is not None:
            raise InvalidDataError("Tag already added to note.")

        new_note_tag = NoteTag(note_id=note.id, tag_id=tag.id)
        db.add(new_note_tag)
        db.commit()
        db.refresh(new_note_tag)
        return new_note_tag

    def read_note_tags(self, db: Session) -> list[NoteTag]:
        result = db.query(NoteTag).all()
        return result

    def update_note_tag(self, note_tag_id: int, note_tag: dict, db: Session) -> NoteTag:
        updating_note_tag = db.query(NoteTag).filter(NoteTag.id == note_tag_id).first()
        if updating_note_tag is None:
            raise ResourceNotFoundError("Note tag not found.")

        note = db.query(Note).filter(Note.id == note_tag["note_id"]).first()
        if note is None:
            raise ResourceNotFoundError("Note not found.")

        tag = db.query(Tag).filter(Tag.id == note_tag["tag_id"]).first()
        if tag is None:
            raise ResourceNotFoundError("Tag not found.")

        existing = (
            db.query(NoteTag)
            .filter(NoteTag.note_id == note.id, NoteTag.tag_id == tag.id)
            .first()
        )
        if existing is not None:
            raise InvalidDataError("Tag already added to note.")

        updating_note_tag.note_id = note.id
        updating_note_tag.tag_id = tag.id
        db.commit()
        db.refresh(updating_note_tag)
        return updating_note_tag

    def delete_note_tag(self, note_tag_id: int, db: Session) -> None:
        deleting_note_tag = db.query(NoteTag).filter(NoteTag.id == note_tag_id).first()
        if deleting_note_tag is None:
            raise ResourceNotFoundError("Note tag not found.")

        db.delete(deleting_note_tag)
        db.commit()


service = Services()


def get_service():
    return service
