import subprocess
import threading

def text_to_siri(text):
    # sayコマンドを使用して、別プロセスで音声を読み上げる
    subprocess.run(["say", text])

def text_to_siri_async(text):
    # 非同期で読み上げを開始
    threading.Thread(target=text_to_siri, args=(text,)).start()