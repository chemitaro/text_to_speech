import json
import requests
import wave
import simpleaudio as sa
import concurrent.futures
import os
import io

def split_text(text, delimiters=("。", "．", ". ", "？", "? ", "！", "! ", "　", "\n")):
    result = [text]
    for delimiter in delimiters:
        temp = []
        for r in result:
            temp.extend([s + delimiter for s in r.split(delimiter) if s])
        result = temp
    return result

def generate_wav(text, speaker=52, filepath='./audio.wav', silence_duration=0.1):
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

    with wave.open(io.BytesIO(response2.content), 'rb') as input_wave:
        framerate = input_wave.getframerate()
        silence_frames = int(framerate * silence_duration)

        input_wave.readframes(silence_frames)
        remaining_frames = input_wave.readframes(input_wave.getnframes() - silence_frames)

        with wave.open(filepath, 'wb') as output_wave:
            output_wave.setnchannels(input_wave.getnchannels())
            output_wave.setsampwidth(input_wave.getsampwidth())
            output_wave.setframerate(input_wave.getframerate())
            output_wave.writeframes(remaining_frames)

def generate_wav_async(text, speaker=52, directory='.'):
    filepath = f"{directory}/audio_{hash(text)}.wav"
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

def text_to_voicevox(text, speaker=52):
    """文字列を音声合成して再生する

    :param text: 読み上げるテキスト
    :type text: str
    :param speaker: キャラクターナンバー, defaults to 52
    :type speaker: int, optional
    """
    splitted_texts = split_text(text)

    directory = "./voicevox"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        audio_file_paths = list(executor.map(generate_wav_async, splitted_texts, [speaker] * len(splitted_texts), [directory] * len(splitted_texts)))

    for audio_file_path in audio_file_paths:
        play_audio(audio_file_path)

    delete_files_in_directory(directory)

if __name__ == '__main__':
    while True:
        print("メッセージを入力してください")
        user_input = input("(終了 or exit で終了): ")

        if user_input.lower() == "終了" or user_input.lower() == "exit":
            break

        print(user_input)
        text_to_voicevox(user_input)