from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..services.author_service import AuthorService

# /authors 以下のエンドポイントをまとめるルーター
router = APIRouter(prefix="/authors", tags=["Authors"])

@router.post("", response_model=schemas.AuthorOut, status_code=201)
def create_author(payload: schemas.AuthorCreate, db: Session = Depends(get_db)):
    service = AuthorService(db)
    return service.create_author(payload)
