from text_to_voicevox import text_to_voicevox_async

if __name__ == "__main__":
    while True:
        print("メッセージを入力してください")
        user_input = input("(終了 or exit で終了): ")

        if user_input.lower() in ["終了", "exit"]:
            break

        print(user_input)
        text_to_voicevox_async(user_input, speaker=52)