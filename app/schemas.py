from pydantic import BaseModel, Field, UUID4, ConfigDict, field_validator
from datetime import datetime

# -------------------------------------------------------------------
# 入力スキーマ: 著者新規作成
# -------------------------------------------------------------------
class AuthorCreate(BaseModel):
    # name は必須(...), 1文字以上50文字以内
    name: str = Field(..., min_length=1, max_length=50)

    @field_validator("name")
    @classmethod
    def trim_name(cls, v: str) -> str:
        # 前後の空白を削除
        v = v.strip()
        # 空文字は許可しない（バリデーションエラーにする）
        if not v:
            raise ValueError("name must not be empty")
        return v

# -------------------------------------------------------------------
# 出力スキーマ: 著者情報
# -------------------------------------------------------------------
class AuthorOut(BaseModel):
    id: UUID4
    name: str
    created_at: datetime
    updated_at: datetime

    # ORM モデルから直接属性を読み取れるようにする設定
    model_config = ConfigDict(from_attributes=True)

# -------------------------------------------------------------------
# 入力スキーマ: 書籍新規作成
# -------------------------------------------------------------------
class BookCreate(BaseModel):
    # title は必須, 1文字以上100文字以内
    title: str = Field(..., min_length=1, max_length=100)
    # 著者IDは UUID4 形式を強制
    author_id: UUID4

    @field_validator("title")
    @classmethod
    def trim_title(cls, v: str) -> str:
        # 前後の空白を削除
        v = v.strip()
        # 空文字は許可しない
        if not v:
            raise ValueError("title must not be empty")
        return v

# -------------------------------------------------------------------
# 出力スキーマ: 書籍情報
# -------------------------------------------------------------------
class BookOut(BaseModel):
    id: UUID4
    title: str
    author_id: UUID4
    author_name: str  # JOINした著者名をレスポンスに含める
    created_at: datetime
    updated_at: datetime

    # ORM モデルから直接属性を読み取れるようにする設定
    model_config = ConfigDict(from_attributes=True)
