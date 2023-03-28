import requests
import json
from base64 import b64decode

# VOICEVOXのAPIエンドポイント
url = "http://127.0.0.1:50021/audio_query"  # 実際のVOICEVOX APIエンドポイントに置き換えてください

# テキストを読み上げるためのデータ
data = {
    "text": "こんにちは、これはVOICEVOXのAPIを使用して読み上げられています。",
    "speaker": "1"  # 使用する話者のID（0から始まる整数）
}

# APIへのリクエストを送信
response = requests.post(url, json=data)

# レスポンスが正常かどうか確認
if response.status_code == 200:
    # JSONレスポンスを解析
    response_data = json.loads(response.text)

    # 音声データ（Base64形式）をデコード
    audio_data = b64decode(response_data["audio_data"])

    # 音声データをファイルに保存
    with open("output.wav", "wb") as audio_file:
        audio_file.write(audio_data)

    print("音声ファイルが正常に生成されました。")
else:
    print("エラーが発生しました。ステータスコード:", response.status_code)