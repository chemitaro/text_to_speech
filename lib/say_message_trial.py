import subprocess
import threading
import keyboard

def text_to_speech(text, stop_event):
    process = subprocess.Popen(["say", text])
    while process.poll() is None:
        if stop_event.is_set():
            process.terminate()
            break

def speech_thread(text):
    stop_event = threading.Event()
    thread = threading.Thread(target=text_to_speech, args=(text, stop_event))
    thread.start()
    keyboard.wait("enter")
    stop_event.set()
    thread.join()

if __name__ == "__main__":
    while True:
        print("メッセージを入力してください")
        user_input = input("(終了 or exit で終了): ")
        if user_input.lower() in ["終了", "exit"]:
            break
        print(user_input)
        speech_thread(user_input)
