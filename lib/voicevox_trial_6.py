import json
import requests
import wave
import simpleaudio as sa
import concurrent.futures

def split_text(text, delimiter="。"):
    return [chunk + delimiter for chunk in text.split(delimiter) if chunk]

def generate_wav(text, speaker=1, filepath='./audio.wav'):
    host = '127.0.0.1'
    port = 50021
    params = (
        ('text', text),
        ('speaker', speaker),
    )
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    headers = {'Content-Type': 'application/json',}
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )
    print("OK 200")

    wf = wave.open(filepath, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(response2.content)
    wf.close()

def play_audio(filepath):
    wave_obj = sa.WaveObject.from_wave_file(filepath)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def generate_and_play(text):
    filepath = f'./audio_{hash(text)}.wav'
    generate_wav(text, filepath=filepath)
    play_audio(filepath)

if __name__ == '__main__':
    while True:
        print("メッセージを入力してください")
        user_input = input("(終了 or exit で終了): ")

        if user_input.lower() == "終了" or user_input.lower() == "exit":
            break

        splitted_texts = split_text(user_input)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(generate_and_play, splitted_texts)