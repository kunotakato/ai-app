import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def generate_resume(prompt):
    """
    OpenAI APIを使って職務経歴書を生成する関数です。
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY が設定されていません。"
            ".envファイルにAPIキーを設定してください。"
        )

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "あなたは職務経歴書作成に強いキャリアアドバイザーです。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content