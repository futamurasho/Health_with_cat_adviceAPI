from sqlalchemy import create_engine,text

# 環境変数から読み込む場合
from dotenv import load_dotenv
import os

load_dotenv()  # .envファイルを読み込む
DATABASE_URL = os.getenv("DATABASE_URL")  # .envファイルに記載された接続情報を取得

# SQLAlchemyエンジンを作成
engine = create_engine(DATABASE_URL)

# 接続確認コード
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE();"))
            print(f"Connected to database: {result.scalar()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()

