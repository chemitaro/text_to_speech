import subprocess
import threading

def text_to_speech(text):
    # sayコマンドを使用して、別プロセスで音声を読み上げる
    subprocess.run(["say", text])

def input_loop():
    while True:
        print("メッセージを入力してください")
        user_input = input("(終了 or exit で終了): ")

        if user_input.lower() in ["終了", "exit"]:
            break

        print(user_input)
        # 非同期で読み上げを開始
        threading.Thread(target=text_to_speech, args=(user_input,)).start()

if __name__ == "__main__":
    input_loop()