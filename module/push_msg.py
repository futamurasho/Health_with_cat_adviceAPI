from module.generate_summary import generate_summary
from database.get_data import get_data
from database.update import update
import requests
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
import os
# LINE Messaging APIのチャンネルアクセストークン
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not LINE_CHANNEL_ACCESS_TOKEN:
    raise Exception("LINE_CHANNEL_ACCESS_TOKEN is not set in .env")

headers = {
    "Content_Type": "application/json",
    "Authorization": "Bearer " + LINE_CHANNEL_ACCESS_TOKEN
    }

def SendMsg(text,uid):
    res = requests.post("https://api.line.me/v2/bot/message/push", 
                        headers=headers, 
                        json={
                            "to": uid,
                            "messages": [{
                                            "type": "text",
                                            "text": text
                                        }]
                        }
                        ).json()


async def process_user(line_id):
    """
    各ユーザーに対するアドバイス生成と送信を処理
    """
    try:
        # データを取得
        user_data = get_data(line_id)

        # アドバイスを生成
        summary = generate_summary(user_data)
        
        # summaryがリスト形式で2要素あるか確認
        if not (isinstance(summary, list) and len(summary) == 2):
            raise ValueError(f"Invalid summary format for {line_id}: {summary}")

        # スコアとアドバイスを抽出
        score, advice = summary

        # データベースを更新
        update(line_id, advice, score)

        # LINEユーザーにメッセージを送信
        SendMsg(advice, line_id)

        return {"line_id": line_id, "status": "success", "advice": advice}

    except linebot.exceptions.LineBotApiError as e:
        # LINE Messaging APIのエラーを特定して記録
        return {"line_id": line_id, "status": "failure", "error": f"LineBotApiError: {e.message}"}

    except Exception as e:
        # その他のエラーを記録
        return {"line_id": line_id, "status": "failure", "error": str(e)}