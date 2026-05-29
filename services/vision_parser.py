import base64
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def encode_image_to_base64(image_file):
    """
    アップロードされた画像ファイルをBase64形式に変換します。
    OpenAI APIに画像を送るための下準備です。
    """
    image_bytes = image_file.getvalue()
    return base64.b64encode(image_bytes).decode("utf-8")


def extract_job_posting_from_image(image_file):
    """
    求人票スクショ画像から、求人情報を読み取る関数です。
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY が設定されていません。.envファイルを確認してください。"
        )

    client = OpenAI(api_key=api_key)

    base64_image = encode_image_to_base64(image_file)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "あなたは求人票画像を読み取り、転職活動に必要な情報を整理する専門家です。",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
この画像は求人票のスクリーンショットです。
画像内の文字を読み取り、以下の形式で整理してください。

# 求人票読み取り結果

## 職種名
## 仕事内容
## 必須スキル
## 歓迎スキル
## 求める人物像
## 勤務条件
## この求人で評価されそうな経験
## 職務経歴書で強調すべきポイント

注意：
- 画像から読み取れない情報は「読み取り不可」と書いてください
- 勝手に情報を作らないでください
- 転職書類作成に使いやすい形で整理してください
""",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        },
                    },
                ],
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content