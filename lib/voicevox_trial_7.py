import json
import requests
import wave
import simpleaudio as sa
import concurrent.futures
import os

def split_text(text, delimiters=("。", "．", ". ", "？", "? ", "！", "! ", "　", "\n")):
    result = [text]
    for delimiter in delimiters:
        temp = []
        for r in result:
            temp.extend([s + delimiter for s in r.split(delimiter) if s])
        result = temp
    return result

def generate_wav(text, speaker=19, filepath='./audio.wav'):
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

    wf = wave.open(filepath, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(response2.content)
    wf.close()

def generate_wav_async(text, speaker=19):
    filepath = f'./voicevox/audio_{hash(text)}.wav'
    generate_wav(text, speaker, filepath)
    return filepath

def play_audio(filepath):
    wave_obj = sa.WaveObject.from_wave_file(filepath)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    while True:
        print("メッセージを入力してください")
        user_input = input("(終了 or exit で終了): ")

        if user_input.lower() == "終了" or user_input.lower() == "exit":
            break

        print(user_input)

        splitted_texts = split_text(user_input)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            audio_file_paths = list(executor.map(generate_wav_async, splitted_texts))

        for audio_file_path in audio_file_paths:
            play_audio(audio_file_path)

        delete_files_in_directory("./voicevox")