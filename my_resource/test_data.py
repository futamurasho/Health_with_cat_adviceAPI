test_data={
    "age":"20",
    "height":"160",
    "times_of_meal":"3",
    "times_of_motion":"4",
    "records_of_meal": {
        "Sunday": {
            "breakfast": "パンと卵",
            "lunch": "サラダとチキン",
            "dinner": "魚とご飯"
        },
        "Monday": {
            "breakfast": "シリアル",
            "lunch": "ハンバーグ",
            "dinner": "カレーライス"
        },
        "Tuesday": {
            "breakfast": "トーストとヨーグルト",
            "lunch": "スパゲッティ",
            "dinner": "豚肉と野菜炒め"
        },
        "Wednesday": {
            "breakfast": "和食(ご飯、味噌汁、卵焼き)",
            "lunch": "ラーメン",
            "dinner": "チキンステーキ"
        },
        "Thursday": {
            "breakfast": "パンケーキ",
            "lunch": "牛丼",
            "dinner": "お刺身と味噌汁"
        },
        "Friday": {
            "breakfast": "クロワッサン",
            "lunch": "魚の煮付け",
            "dinner": "ピザ"
        },
        "Saturday": {
            "breakfast": "フルーツとスムージー",
            "lunch":"焼きそば",
            "dinner": "鍋料理"
        }
    },
    "records_of_motion":{
        "Sunday":3,
        "Monday":4,
        "Tuesday":3,
        "Wednesday":2,
        "Thursday":2,
        "Friday":4,
        "Saturday":5
    },
    "previous_records_of_meal": {
        "Monday": {"breakfast": "トースト"},
        "Tuesday": {"breakfast": "卵", "lunch": "サラダ"},
        "Wednesday": {"lunch": "パスタ"},
        "Thursday": {},
        "Friday": {"dinner": "ピザ"},
        "Saturday": {},
        "Sunday": {"breakfast": "オートミール", "dinner": "スープ"}
    },
    "previous_records_of_motion": {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 1,
        "Thursday": 1,
        "Friday": 2,
        "Saturday": 1,
        "Sunday": 1
    }
}

test_data_low = {
    "records_of_meal": {
        "Monday": {"breakfast": "トースト"},
        "Tuesday": {"breakfast": "卵", "lunch": "サラダ"},
        "Wednesday": {"lunch": "パスタ"},
        "Thursday": {},
        "Friday": {"dinner": "ピザ"},
        "Saturday": {},
        "Sunday": {"breakfast": "オートミール", "dinner": "スープ"}
    },
    "records_of_motion": {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 1,
        "Thursday": 1,
        "Friday": 2,
        "Saturday": 1,
        "Sunday": 1
    },
    "previous_records_of_meal": {
        "Monday": {},
        "Tuesday": {},
        "Wednesday": {},
        "Thursday": {},
        "Friday": {},
        "Saturday": {},
        "Sunday": {}
    },
    "previous_records_of_motion": {
        "Monday": 1,
        "Tuesday": 1,
        "Wednesday": 1,
        "Thursday": 1,
        "Friday": 1,
        "Saturday": 1,
        "Sunday": 1
    }
}
