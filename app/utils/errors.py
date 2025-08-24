from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# -------------------------------------------------------------------
# 共通のエラーレスポンス生成関数
# -------------------------------------------------------------------
def error_response(code: str, message: str, status: int, details=None):
    # JSON 形式で統一されたエラーを返す
    # - code: エラー種別（HTTP_ERROR, VALIDATION_ERROR など）
    # - message: エラー概要
    # - details: バリデーションエラーの詳細（フィールドごとの情報）
    return JSONResponse(
        status_code=status,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": details or [],
            }
        },
    )

# -------------------------------------------------------------------
# HTTPException 用のハンドラ
# 例: raise HTTPException(status_code=404, detail="Book not found")
# → {"error": {"code": "HTTP_ERROR", "message": "Book not found", "details": []}}
# -------------------------------------------------------------------
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return error_response(
        code="HTTP_ERROR",
        message=str(exc.detail),
        status=exc.status_code,
    )

# -------------------------------------------------------------------
# バリデーションエラー用のハンドラ
# FastAPI/Pydantic が自動で検出した入力エラー（422）を整形する
# 例: {"field": "body.name", "message": "Field required"}
# -------------------------------------------------------------------
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = []
    for e in exc.errors():
        # loc: エラーが起きた場所（body.name / query.id など）
        loc = ".".join([str(x) for x in e.get("loc", [])])
        msg = e.get("msg", "")
        details.append({"field": loc, "message": msg})

    return error_response(
        code="VALIDATION_ERROR",
        message="Request validation failed",
        status=422,
        details=details,
    )

