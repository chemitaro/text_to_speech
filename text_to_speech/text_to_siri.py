import subprocess
import threading
from .preprocess import omit_code, omit_url

def text_to_siri(text):
    # sayコマンドを使用して、別プロセスで音声を読み上げる
    text = omit_code(text)
    text = omit_url(text)
    subprocess.run(["say", text])

def text_to_siri_async(text):
    # 非同期で読み上げを開始
    threading.Thread(target=text_to_siri, args=(text,)).start()