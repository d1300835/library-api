# app/services/author_service.py
from sqlalchemy.orm import Session
from .. import models, schemas

class AuthorService:
    def __init__(self, db: Session):
        self.db = db

    def create_author(self, payload: schemas.AuthorCreate):
        # 1) Pydantic でバリデーション済みの入力データを受け取る
        #    （AuthorCreate: name は必須・最大50文字）
    
        # 2) ORM モデルのインスタンスを生成
        author = models.Author(name=payload.name)

        # 3) DBに追加
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)

        # 4) レスポンススキーマ（AuthorOut）に変換して返す
        return author
