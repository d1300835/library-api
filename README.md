# Library API (FastAPI + MySQL)

書籍とその著者を管理するためのシンプルな図書APIです。

FastAPI / MySQL を使用し、Docker Compose による環境構築をサポートしています。

---

## ＜開発環境セットアップ手順＞

### 前提

- Docker / Docker Compose がインストールされていること
  
  ### 起動方法
  
  ```bash
  # リポジトリをクローン
  git clone https://github.com/username/library-api.git
  cd library-api
  # ビルド & 起動
  docker compose up --build
  ```
  
  ### アクセス

- API: [http://localhost:8000](http://localhost:8000)

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ＜API エンドポイント一覧＞

### 1. 著者登録

```bash
curl -X POST http://localhost:8000/authors   -H "Content-Type: application/json"   -d '{"name": "夏目漱石"}'
```

レスポンス例:

```json
{
  "id": "8b0d2c91-9d8c-4b5e-9ad6-6f6a33b4f5d9",
  "name": "夏目漱石",
  "created_at": "2025-08-24T10:30:00Z",
  "updated_at": "2025-08-24T10:30:00Z"
}
```

### 2. 書籍登録

```bash
curl -X POST http://localhost:8000/books   -H "Content-Type: application/json"   -d '{"title": "坊っちゃん", "author_id": "8b0d2c91-9d8c-4b5e-9ad6-6f6a33b4f5d9"}'
```

レスポンス例:

```json
{
  "id": "a1f2d9c8-7e6b-4d55-9a21-4f2a6b0d8e3a",
  "title": "坊っちゃん",
  "author_id": "8b0d2c91-9d8c-4b5e-9ad6-6f6a33b4f5d9",
  "author_name": "夏目漱石",
  "created_at": "2025-08-24T10:31:00Z",
  "updated_at": "2025-08-24T10:31:00Z"
} 
```

### 3. 書籍一覧

```bash
curl "http://localhost:8000/books?offset=0&limit=10"
```

レスポンス例:

```json
[
  {
    "id": "a1f2d9c8-7e6b-4d55-9a21-4f2a6b0d8e3a",
    "title": "坊っちゃん",
    "author_id": "8b0d2c91-9d8c-4b5e-9ad6-6f6a33b4f5d9",
    "author_name": "夏目漱石",
    "created_at": "2025-08-24T10:31:00Z",
    "updated_at": "2025-08-24T10:31:00Z"
  },
  {
    "id": "c2e3f9a7-1a6d-4e21-9f56-3a6f1b2d9c1e",
    "title": "吾輩は猫である",
    "author_id": "8b0d2c91-9d8c-4b5e-9ad6-6f6a33b4f5d9",
    "author_name": "夏目漱石",
    "created_at": "2025-08-24T10:32:00Z",
    "updated_at": "2025-08-24T10:32:00Z"
  },
  {
    "id": "d3f4e0b8-2b7e-4c32-8a67-4b7f2c3e0d2f",
    "title": "こころ",
    "author_id": "8b0d2c91-9d8c-4b5e-9ad6-6f6a33b4f5d9",
    "author_name": "夏目漱石",
    "created_at": "2025-08-24T10:33:00Z",
    "updated_at": "2025-08-24T10:33:00Z"
  }
]
```

レスポンスヘッダー例:

```json
X-Total-Count: 3
X-Offset: 0
X-Limit: 10
```

### 4. 書籍詳細

```bash
curl http://localhost:8000/books/a1f2d9c8-7e6b-4d55-9a21-4f2a6b0d8e3a
```

レスポンス例:

```json
{
  "id": "a1f2d9c8-7e6b-4d55-9a21-4f2a6b0d8e3a",
  "title": "坊っちゃん",
  "author_id": "8b0d2c91-9d8c-4b5e-9ad6-6f6a33b4f5d9",
  "author_name": "夏目漱石",
  "created_at": "2025-08-24T10:31:00Z",
  "updated_at": "2025-08-24T10:31:00Z"
}
```

---

### 5. 書籍削除

```bash
curl -X DELETE http://localhost:8000/books/a1f2d9c8-7e6b-4d55-9a21-4f2a6b0d8e3a -i
```

レスポンス例:

```
HTTP/1.1 204 No Content
```

---

## ＜アーキテクチャの考慮点＞

### 環境構築の容易性

- Docker Compose を利用し、`git clone` + `docker compose up --build` だけで API と MySQL が起動可能。追加設定不要ですぐに動作します。

### データベース管理

- ORM: SQLAlchemy を使用。
- インデックス・制約を設計に反映
  - `(author_id, title)` にユニーク制約
  - `Book.title` / `Author.name` にインデックス

### 堅牢性

- **入力検証**: Pydantic により必須項目・文字数制約を自動チェック。
  - 著者名: 必須、最大 50 文字
  - 書籍タイトル: 必須、最大 100 文字
- **エラーハンドリング**
  - 422 Unprocessable Entity: バリデーションエラー
  - 400 Bad Request: 存在しない著者 ID を指定した場合
  - 404 Not Found: 存在しない書籍/著者にアクセスした場合
  - 409 Conflict: 著者ごとに同一タイトルの本を登録した場合

### 設計（Separation of Concerns）

- `app/models.py`: DB モデル定義 (SQLAlchemy)
- `app/schemas.py`: 入出力スキーマ定義 (Pydantic)
- `app/routers/*.py`: エンドポイントごとのルーティング
- `app/database.py`: DB セッション管理
- `app/main.py`: FastAPI アプリ本体

→ 関心ごとを分離し、可読性・保守性を向上。

---

## ＜ディレクトリ構成＞

```
.
library-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── utils/
│   │   └── errors.py
│   └── routers/
│       ├── authors.py
│       └── books.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

#### ＜未実装機能・今後の検討事項＞

※ 今回のコーディング課題のスコープ外として未対応ですが、実務を想定すると以下が必要になります。

### 本番運用に向けたDB設計

- 開発環境では MySQL コンテナを利用
- 本番ではマネージド DB (例: AWS RDS) の利用を想定
- 接続情報（Host, User, Password 等）は Secrets Manager / Parameter Store などクラウドのセキュアストレージで管理

### デプロイ / 運用

（例）

- コンテナ実行環境: AWS App Runner
- コンテナレジストリ: Amazon ECR
- CI/CD パイプラインによる自動デプロイ

### 機能拡張

- API ユーザー認証・ユーザー管理
- ログ出力（構造化ログ、監査ログなど）
