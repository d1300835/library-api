from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from .. import models, schemas

class BookService:
    def __init__(self, db: Session):
        self.db = db

    # -------------------------------------------------------------------
    # POST /books : 書籍を新規登録
    # -------------------------------------------------------------------
    def create_book(self, payload: schemas.BookCreate):
        # 1) 著者が存在するかチェック
        author = self.db.get(models.Author, str(payload.author_id))
        if not author:
            # 指定された著者IDが存在しなければ 400 Bad Request
            raise HTTPException(status_code=400, detail="author_id not found")

        # 2) 同一著者に同じタイトルの本が既にあるか確認
        dup = self.db.execute(
            select(models.Book).where(
                models.Book.author_id == str(payload.author_id),
                models.Book.title == payload.title
            )
        ).scalars().first()
        if dup:
            # 重複登録は 409 Conflict
            raise HTTPException(status_code=409, detail="This author already has a book with that title")

        # 3) 新規レコードを作成
        book = models.Book(title=payload.title, author_id=str(payload.author_id))
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book) # INSERT後の自動採番やタイムスタンプを反映

        # 4) レスポンス用スキーマに詰めて返す
        return schemas.BookOut(
            id=book.id,
            title=book.title,
            author_id=book.author_id,
            author_name=author.name,
            created_at=book.created_at,
            updated_at=book.updated_at
        )

    # -------------------------------------------------------------------
    # GET /books : 書籍一覧を取得
    # -------------------------------------------------------------------
    def list_books(self):
        # 著者名を JOIN して取得
        stmt = select(models.Book, models.Author.name).join(
            models.Author, models.Book.author_id == models.Author.id
        )
        rows = self.db.execute(stmt).all()

        # JOIN結果を Pydantic モデルに詰め替えて返す
        return [
            schemas.BookOut(
                id=r.Book.id,
                title=r.Book.title,
                author_id=r.Book.author_id,
                author_name=r.name,
                created_at=r.Book.created_at,
                updated_at=r.Book.updated_at
            )
            for r in rows
        ]

    # -------------------------------------------------------------------
    # GET /books/{book_id} : 書籍詳細を取得
    # -------------------------------------------------------------------
    def get_book(self, book_id: str):
        # 著者名を JOIN して1件取得
        stmt = (
            select(models.Book, models.Author.name)
            .join(models.Author, models.Book.author_id == models.Author.id)
            .where(models.Book.id == book_id)
        )
        row = self.db.execute(stmt).first()
        if not row:
            # 存在しない場合は 404 Not Found
            raise HTTPException(status_code=404, detail="Book not found")

        # JOIN結果を Pydantic モデルに詰め替えて返す
        return schemas.BookOut(
            id=row.Book.id,
            title=row.Book.title,
            author_id=row.Book.author_id,
            author_name=row.name,
            created_at=row.Book.created_at,
            updated_at=row.Book.updated_at
        )

    # -------------------------------------------------------------------
    # DELETE /books/{book_id} : 書籍を削除
    # -------------------------------------------------------------------
    def delete_book(self, book_id: str):
        # 1) 削除対象を取得
        book = self.db.get(models.Book, book_id)
        if not book:
            # 存在しない場合は 404 Not Found
            raise HTTPException(status_code=404, detail="Book not found")
        
        # 2) 削除 → コミット
        self.db.delete(book)
        self.db.commit()

        # 3) 204 No Content（ボディ無し）を返す
        return None
