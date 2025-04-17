from openai import OpenAI
from dotenv import load_dotenv
import ast
import os
from .chain_initializer import initialize_chain
# .envファイルの読み込み
load_dotenv()
client = OpenAI()

# 文字列をリストに変換（エラーの場合エラー表示）
def parse_content(content):
    try:
        # 全角のマイナス記号（U+2212）を半角のマイナス（-）に置き換え
        normalized_content = content.replace('−', '-')
        return ast.literal_eval(normalized_content)
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing content: {e}")
        return None

#食事（朝食・昼食・夕食）と運動データをもとに総評を生成する関数
#必須データ(age,height,times of meal,times of motion,records of meal,records of motion)
def generate_summary(user_data):
    # 運動記録の説明対応表
    motion_descriptions = {
        5: "1時間以上運動した",
        4: "30分～1時間運動した",
        3: "20分ウォーキングを行った",
        2: "10分歩いた",
        1: "全く動いていない"
    }

    try:
        # 食事データをフォーマット
        meal_records = "\n".join([
            f"{day}: 朝食: {meals.get('breakfast', '食べなかった')}, 昼食: {meals.get('lunch', '食べなかった')}, 夕食: {meals.get('dinner', '食べなかった')}"
            for day, meals in user_data['records_of_meal'].items()
        ])

        # 先週のデータが空かどうかを判定
        previous_meal_records = user_data.get('previous_records_of_meal', {})
        is_previous_meal_records_empty = all(not meals for meals in previous_meal_records.values())
        
        # 運動データを説明に変換してフォーマット
        motion_records = "\n".join([
            f"{day}: {motion_descriptions[motions]}"
            for day, motions in user_data['records_of_motion'].items()
        ])

        # 運動データを説明に変換してフォーマット
        previous_motion_records = "\n".join([
            f"{day}: {motion_descriptions[motions]}"
            for day, motions in user_data['previous_records_of_motion'].items()
        ])



        # 欠けているデータを確認
        age = user_data.get("age")
        height = user_data.get("height")
        times_of_meal = user_data.get("times_of_meal")
        times_of_motion = user_data.get("times_of_motion")

        # 動的にプロンプトを作成
        prompt_parts = ["まず，ユーザーの健康データです。\n性別: 女性"]

        if age:
            prompt_parts.append(f"年齢: {age}歳")
        if height:
            prompt_parts.append(f"身長: {height}cm")
        if times_of_meal:
            prompt_parts.append(f"1日の平均食事回数: {times_of_meal}回")
        if times_of_motion:
            prompt_parts.append(f"1週間の平均運動回数: {times_of_motion}回")

        prompt_parts.append(f"1週間の食事記録:\n{meal_records}")
        prompt_parts.append(f"1週間の運動記録:\n{motion_records}")

        # 先週の記録をプロンプトに含める条件
        if not is_previous_meal_records_empty :
            formatted_previous_meal_records = "\n".join([
                f"{day}: 朝食: {meals.get('breakfast', '食べなかった')}, 昼食: {meals.get('lunch', '食べなかった')}, 夕食: {meals.get('dinner', '食べなかった')}"
                for day, meals in previous_meal_records.items()
            ])
            prompt_parts.append(f"先週の食事記録:\n{formatted_previous_meal_records}")
            prompt_parts.append(f"先週の運動記録:\n{previous_motion_records}")
            prompt_parts.append(
                """
                これらを基に、1週間の食事と運動に関して-5以上5以下の整数で評価してください。そして、できるだけ誉めながら200文字以内で先週との違いを踏まえて運動と食事の評価と栄養に関するアドバイスを行なってください。
                点数がマイナスの場合は、何が良くなかったのかを伝えてください。また、食事回数が少ない日が多い場合は点数を低くしましょう。評価内容とアドバイスでは評価点には言及しないでください。
                出力形式は以下のようなリストにしてください。従わなければ、罰を受けます。
                [(評価点),(評価内容とアドバイス)]
                出力例は次のようなものです
                [3,"素晴らしい食事と運動のバランスです！特に魚や野菜を取り入れている点が良いですね。タンパク質やビタミンを意識して、フルーツやナッツも加えるとさらに栄養価がアップします"]
                """
            )
        else:
            # 先週のデータが無視される場合のプロンプト
            prompt_parts.append(
                """
                これらを基に、1週間の食事と運動に関して-5以上5以下の整数で評価してください。そして、できるだけ誉めながら200文字以内で運動と食事の評価と栄養に関するアドバイスを行なってください。
                点数がマイナスの場合は、何が良くなかったのかを伝えてください。また、食事回数が少ない日が多い場合は点数を低くしましょう。評価内容とアドバイスでは評価点には言及しないでください。
                出力形式は以下のようなリストにしてください。従わなければ、罰を受けます。
                [(評価点),(評価内容とアドバイス)]
                出力例を二つ挙げます。
                [3,"素晴らしい食事と運動のバランスです！特に魚や野菜を取り入れている点が良いですね。タンパク質やビタミンを意識して、フルーツやナッツも加えるとさらに栄養価がアップします"]
                [-5,"食事と運動の記録が非常に少ないですね。栄養をしっかり摂ることが大切です。毎日3食を心がけ、特にフルーツや野菜を取り入れると良いでしょう。ビタミンCが豊富な食材を選ぶと、免疫力も高まります。運動も少しずつ取り入れて、体を動かす習慣をつけていきましょう！"]
                """
            )
         # 最終プロンプトを結合
        prompt = "\n".join(prompt_parts)
        # print(prompt)
        chain=initialize_chain()
        max_retries = 3  # リトライ回数の上限
        retry_count = 0
        content = None
        while retry_count < max_retries:
            try:
                # チェーンを呼び出す
                res = chain.invoke(prompt)
                content = res.content.strip()
                print(content)
                content = parse_content(content)
            
                if isinstance(content, list) and len(content) == 2:
                    return content  # 正常なリストが取得できたら返す
            except Exception as e:
                print(f"Error during generation attempt {retry_count + 1}: {e}")
            retry_count += 1
        # ここでリトライ回数を超えた場合にエラーを発生させる
        raise RuntimeError("Failed to generate valid summary after maximum retries.")

    except Exception as e:
        return f"エラーが発生しました: {e}"