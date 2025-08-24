from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

# /authors 以下のエンドポイントをまとめるルーター
router = APIRouter(prefix="/authors", tags=["Authors"])

# -------------------------------------------------------------------
# POST /authors : 著者を新規登録
# -------------------------------------------------------------------
@router.post("", response_model=schemas.AuthorOut, status_code=201)
def create_author(payload: schemas.AuthorCreate, db: Session = Depends(get_db)):
    # 1) Pydantic でバリデーション済みの入力データを受け取る
    #    （AuthorCreate: name は必須・最大50文字）
    
    # 2) ORM モデルのインスタンスを生成
    author = models.Author(name=payload.name)

    # 3) DBに追加
    db.add(author)
    db.commit()       # コミットして確定
    db.refresh(author) # DBが生成した id / timestamp を反映

    # 4) レスポンススキーマ（AuthorOut）に変換して返す
    return author
