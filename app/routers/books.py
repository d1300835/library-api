from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..services.book_service import BookService

# /books 以下のエンドポイントをまとめるルーター
router = APIRouter(prefix="/books", tags=["Books"])

@router.post("", response_model=schemas.BookOut, status_code=201)
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db)):
    return BookService(db).create_book(payload)

@router.get("", response_model=list[schemas.BookOut])
def list_books(db: Session = Depends(get_db)):
    return BookService(db).list_books()

@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: str, db: Session = Depends(get_db)):
    return BookService(db).get_book(book_id)

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: str, db: Session = Depends(get_db)):
    return BookService(db).delete_book(book_id)
