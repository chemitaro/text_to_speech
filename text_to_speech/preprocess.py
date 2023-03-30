"""
読み上げる前のテキストを前処理する
"""
import re

def omit_code(text):
    """コードブロックの中身を音声合成しないようにするため、'コードは省略'に置換する

    :param text: 読み上げるテキスト
    :type text: str
    """
    return re.sub(r'```.*?```', 'コードは省略。', text, flags=re.DOTALL)

def omit_url(text):
    """URLを音声合成しないようにするため、'URL'に置換する

    :param text: 読み上げるテキスト
    :type text: str
    """
    return re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', 'URL', text)