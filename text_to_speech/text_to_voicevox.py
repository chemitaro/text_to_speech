import json
import requests
import wave
import simpleaudio as sa
import concurrent.futures
import threading
import os
import io
import time
import re
from preprocess import omit_code, omit_url

def mkdir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def split_text(text, pattern=r"([。、．！？，\. ,! ,\? ,　,\n])"):
    split_text = re.split(pattern, text)

    # 区切り文字と分割されたテキストを交互に結合してリストに格納
    split_result = []
    for i in range(0, len(split_text) - 1, 2):
        split_result.append(split_text[i] + split_text[i + 1])

    # 最後の要素が区切り文字でない場合、結果に追加
    if not re.fullmatch(pattern, split_text[-1]):
        split_result.append(split_text[-1])

    return split_result

def split_text_and_filepaths(texts, directory='.'):
    result = []
    for text in texts:
        filepath = f'{directory}/audio_{hash(text)}.wav'
        result.append({'text': text, 'filepath': filepath})
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

def generate_wav_async(texts, speakers, filepaths):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for text, speaker, filepath in zip(texts, speakers, filepaths):
            futures.append(executor.submit(generate_wav, text, speaker, filepath))
            time.sleep(0.2)

def play_audio(filepath):
    max_attempts = 100
    attempts = 0

    while not os.path.exists(filepath) and attempts < max_attempts:
        time.sleep(0.2)
        attempts += 1

    if attempts == max_attempts:
        print("エラー: 指定されたファイルが見つかりませんでした。")
        return

    wave_obj = sa.WaveObject.from_wave_file(filepath)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def text_to_voicevox(text, speaker=52, directory="./voicevox_temp"):
    """文字列を音声合成して再生する

    :param text: 読み上げるテキスト
    :type text: str
    :param speaker: キャラクターナンバー, defaults to 52
    :type speaker: int, optional
    :param directory: 一時ファイルを保存するディレクトリ, defaults to "./voicevox"
    :type directory: str, optional
    """
    text = omit_code(text)
    text = omit_url(text)
    splitted_texts = split_text(text)

    # directory の存在を確認し、存在しない場合は作成する
    mkdir(directory)

    text_and_filepaths = split_text_and_filepaths(splitted_texts, directory)

    texts = [d['text'] for d in text_and_filepaths]
    filepaths = [d['filepath'] for d in text_and_filepaths]
    speakers = [speaker] * len(text_and_filepaths)

    threading.Thread(target=generate_wav_async, args=(texts, speakers, filepaths,)).start()

    time.sleep(0.5)

    for audio_file_path in filepaths:
        play_audio(audio_file_path)

    delete_files_in_directory(directory)

def text_to_voicevox_async(text, speaker =52, directory="./voicevox"):
    """文字列を音声合成して再生を非同期でバックグラウンドで行う

    :param text: 読み上げるテキスト
    :type text: str
    :param speaker: キャラクターナンバー, defaults to 52
    :type speaker: int, optional
    :param directory: 一時ファイルを保存するディレクトリ, defaults to "./voicevox"
    :type directory: str, optional
    """
    threading.Thread(target=text_to_voicevox, args=(text, speaker,)).start()