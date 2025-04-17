from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
# 環境変数から読み込む場合
from dotenv import load_dotenv
import os

load_dotenv()  # .envファイルを読み込む
DATABASE_URL = os.getenv("DATABASE_URL")  # .envファイルに記載された接続情報を取得

# SQLAlchemyエンジンを作成
engine = create_engine(DATABASE_URL)

def update(line_id: str, output: str, score: int):
    score_update_query = """
        UPDATE users
        SET score = GREATEST(LEAST(score + :score, 10), -9)  -- スコアを-10から10の範囲内に制限
        WHERE line_id = :line_id;
    """
    try:
        # ユーザーIDを取得
        with engine.begin() as connection:
            #スコア更新
            connection.execute(text(score_update_query), {"score": score, "line_id": line_id})

            #ユーザid取得
            query_get_user_id = "SELECT id FROM users WHERE line_id = :line_id;"
            user_result = connection.execute(text(query_get_user_id), {"line_id": line_id}).fetchone()
            if not user_result:
                raise ValueError(f"User with line_id {line_id} not found.")
            
            user_id = user_result[0]

            # 今日の日付を取得
            today = datetime.now().date()

            # アドバイス保存
            query_insert_output = """
                INSERT INTO chatgpt_outputs (user_id, date, output, score)
                VALUES (:user_id, :date, :output, :score);
            """
            connection.execute(
                text(query_insert_output),
                {"user_id": user_id, "date": today, "output": output, "score": score}
            )
            return {"message": "Update and save successful", "line_id": line_id, "score": score, "output": output}
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

