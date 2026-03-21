from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    notes: Mapped[list["Note"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(String)

    user: Mapped[User] = relationship(back_populates="notes")
    note_tags: Mapped[list["NoteTag"]] = relationship(
        back_populates="note", cascade="all, delete-orphan"
    )


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    note_tags: Mapped[list["NoteTag"]] = relationship(
        back_populates="tag", cascade="all, delete-orphan"
    )


class NoteTag(Base):
    __tablename__ = "note_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    note_id: Mapped[int] = mapped_column(Integer, ForeignKey("notes.id"))
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tags.id"))

    note: Mapped[Note] = relationship(back_populates="note_tags")
    tag: Mapped[Tag] = relationship(back_populates="note_tags")
