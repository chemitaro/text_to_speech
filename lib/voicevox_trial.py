import requests
import json
from base64 import b64decode

#文字列の入力
text = "私の名前はずんだもんです。東北地方の応援マスコットをしています。得意なことはしゃべることです。"
# 音声合成クエリの作成
res1 = requests.post('http://127.0.0.1:50021/audio_query',params = {'text': text, 'speaker': 1})
# 音声合成データの作成
res2 = requests.post('http://127.0.0.1:50021/synthesis',params = {'speaker': 1},data=json.dumps(res1.json()))
# wavデータの生成

print("レスポンス内容:", res2)

if res2.status_code == 200:
    # JSONレスポンスを解析
    response_data = json.loads(res2.text)

    # 音声データ（Base64形式）をデコード
    audio_data = b64decode(response_data["audio_data"])

    # 音声データをファイルに保存
    with open("output.wav", "wb") as audio_file:
        audio_file.write(audio_data)

    print("音声ファイルが正常に生成されました。")
else:
    print("エラーが発生しました。ステータスコード:", res2.status_code)