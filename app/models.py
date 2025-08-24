import uuid
from sqlalchemy import String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base, TimestampMixin

UUID_STR = String(36)

class Author(TimestampMixin, Base):
    __tablename__ = "authors"
    id: Mapped[str] = mapped_column(UUID_STR, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    books: Mapped[list['Book']] = relationship('Book', back_populates='author', cascade='all, delete-orphan')

class Book(TimestampMixin, Base):
    __tablename__ = "books"
    id: Mapped[str] = mapped_column(UUID_STR, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    author_id: Mapped[str] = mapped_column(UUID_STR, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False, index=True)

    author: Mapped['Author'] = relationship('Author', back_populates='books')

    __table_args__ = (
        UniqueConstraint("author_id", "title", name="uq_books_author_title"),
        Index("idx_books_title", "title"),
        Index("idx_books_author_id", "author_id"),
    )
