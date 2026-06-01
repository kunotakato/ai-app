from services.openai_client import get_openai_client


def analyze_self(prompt: str) -> str:
    """
    OpenAI APIを使って自己分析・職種診断を実行します。
    """

    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "あなたは自己分析とキャリア支援に強いキャリアアドバイザーです。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content