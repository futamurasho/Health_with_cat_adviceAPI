import asyncio
from module.push_msg import process_user
from database.get_user_id import get_user_id
from fastapi import FastAPI,HTTPException

app=FastAPI()


@app.post("/")
async def broadcast_advice():
    """
    全ユーザーにアドバイスを生成して送信する（並列処理版）
    """
    try:
        # 全ユーザーのuser_idを取得
        user_ids = get_user_id()
        if not user_ids:
            return {"message": "No users found in the database"}

        # 並列処理タスクを作成
        tasks = [process_user(line_id) for line_id in user_ids]
        
        # 並列で全タスクを実行
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 成功と失敗を集計
        success_count = sum(1 for result in results if isinstance(result, dict) and result["status"] == "success")
        failure_count = len(results) - success_count

        return {
            "message": "Broadcast completed",
            "success_count": success_count,
            "failure_count": failure_count,
            "details": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# # テスト
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

