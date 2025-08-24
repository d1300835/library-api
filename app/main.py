from fastapi import FastAPI
from .database import Base, engine
from .routers import authors, books
from .utils.errors import http_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="Library API", version="1.0.0")

# 起動時にテーブル作成(存在しないテーブルだけ)
Base.metadata.create_all(bind=engine)

# エラーハンドラを追加
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# ルーター登録 (/authors と /books)
app.include_router(authors.router)
app.include_router(books.router)

# ヘルスチェック用エンドポイント
@app.get("/healthz", tags=["Health"])
def healthz():
    return {"status": "ok"}
