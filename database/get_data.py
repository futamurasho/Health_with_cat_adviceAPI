from sqlalchemy import create_engine,text
from datetime import datetime, timedelta
from decimal import Decimal
import json
# 環境変数から読み込む場合
from dotenv import load_dotenv
import os

load_dotenv()  # .envファイルを読み込む
DATABASE_URL = os.getenv("DATABASE_URL")  # .envファイルに記載された接続情報を取得

# SQLAlchemyエンジンを作成
engine = create_engine(DATABASE_URL)

#健康データ取得
def fetch_health_data(user_id, start_date, end_date):
    query = """
        SELECT date, breakfast, lunch, dinner, exercise
        FROM health_data
        WHERE user_id = :user_id AND date BETWEEN :start_date AND :end_date;
    """
    with engine.connect() as connection:
        result = connection.execute(
            text(query), {"user_id": user_id, "start_date": start_date, "end_date": end_date}
        )
        
        days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        records_of_meal = {day: {} for day in days_of_week}
        records_of_motion = {day: 1 for day in days_of_week}

        for row in result:
            row_data = row._mapping
            date_str = row_data["date"].strftime('%A')  # 曜日を取得
            
            # JSONデータを安全にリストへ変換し、文字列化
            def json_to_string(json_data):
                if json_data:  # JSONデータが存在する場合
                    try:
                        items = json.loads(json_data)  # JSONをリストにデコード
                        if isinstance(items, list):  # リストであることを確認
                            return ",".join(items)
                        else:
                            return "データ形式エラー"  # リスト以外の場合のエラーメッセージ
                    except json.JSONDecodeError:
                        return "データ形式エラー"  # JSONデコードエラー時
                else:
                    return "食べなかった"

            records_of_meal[date_str] = {
                "breakfast": json_to_string(row_data["breakfast"]),
                "lunch": json_to_string(row_data["lunch"]),
                "dinner": json_to_string(row_data["dinner"]),
            }
            records_of_motion[date_str] = row_data["exercise"] or 1

        return {
            "records_of_meal": records_of_meal,
            "records_of_motion": records_of_motion,
        }




def fetch_user_info_by_line_id(line_id):
    """LINE IDでユーザー情報を取得"""
    query = "SELECT id, age, height, times_of_meal, times_of_motion FROM users WHERE line_id = :line_id;"
    with engine.connect() as connection:
        result = connection.execute(text(query), {"line_id": line_id}).fetchone()
        if result:  # データが存在する場合
            user_info = dict(result._mapping)
            # Decimal型を文字列に変換
            if isinstance(user_info.get("height"), Decimal):
                user_info["height"] = str(user_info["height"])
            return user_info
        else:
            return None  # データが存在しない場合はNoneを返す

def get_data(line_id):
    """LINE IDを利用して1週間分のデータを整形して返す"""
    today = datetime.today().date()

    # 今日を基準に今週の開始日と終了日を計算
    this_week_end = today  # 今日を今週の終了日とする
    this_week_start = this_week_end - timedelta(days=6)  # 今週の開始日は終了日の6日前

    # 先週の開始日と終了日を計算
    last_week_end = this_week_start - timedelta(days=1)  # 先週の終了日は今週開始日の前日
    last_week_start = last_week_end - timedelta(days=6)  # 先週の開始日は終了日の6日前

    # ユーザー情報を取得
    user_info = fetch_user_info_by_line_id(line_id)
    if not user_info:
        raise ValueError(f"User with line_id '{line_id}' not found.")

    user_id = user_info["id"]  # `user_id`を取得

    # 現在の週と先週のデータを取得
    current_week_data = fetch_health_data(user_id, this_week_start, this_week_end)
    previous_week_data = fetch_health_data(user_id, last_week_start, last_week_end)

    # user_data形式に整形
    user_data = {
        "age": user_info.get("age"),
        "height": user_info.get("height"),
        "times_of_meal": user_info.get("times_of_meal"),
        "times_of_motion": user_info.get("times_of_motion"),
        "records_of_meal": current_week_data["records_of_meal"],  # 現在の週の食事データ
        "records_of_motion": current_week_data["records_of_motion"],  # 現在の週の運動データ
        "previous_records_of_meal": previous_week_data["records_of_meal"],  # 先週の食事データ
        "previous_records_of_motion": previous_week_data["records_of_motion"],  # 先週の運動データ
    }
    return user_data

