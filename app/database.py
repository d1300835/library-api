import os
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy import DateTime
from dotenv import load_dotenv

# ローカル開発では .env を読む
load_dotenv() 
DATABASE_URL = os.environ["DATABASE_URL"]

# DBエンジンを作成する
engine = create_engine(DATABASE_URL, echo=False, future=True, pool_pre_ping=True)
# Sessionを作成する
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# 全モデル共通のベースクラス
class Base(DeclarativeBase):
    pass

# 共通カラム(created_at / updated_at)の定義
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

# 依存性注入：リクエスト単位のセッション
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
