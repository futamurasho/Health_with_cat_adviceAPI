import os
from sqlalchemy import create_engine,text
# 環境変数から読み込む場合
from dotenv import load_dotenv


load_dotenv()  # .envファイルを読み込む
DATABASE_URL = os.getenv("DATABASE_URL")  # .envファイルに記載された接続情報を取得

# SQLAlchemyエンジンを作成
engine = create_engine(DATABASE_URL)


def get_user_id():
    """
    データベースから全てのユーザーID（line_id）を取得し、リストで返す関数
    """
    user_ids = []
    try:
        with engine.connect() as connection:
            query = "SELECT line_id FROM users"
            result = connection.execute(text(query))
            # `row`がタプルの場合に対応
            user_ids = [row[0] for row in result]  # 0番目の要素がline_id
    except Exception as e:
        print(f"Error fetching user IDs: {e}")
    
    return user_ids