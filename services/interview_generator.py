from services.openai_client import get_openai_client


def generate_interview_prep(prompt: str) -> str:
    """
    OpenAI APIを使って面接対策を生成します。
    """

    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "あなたは転職面接対策に強いキャリアアドバイザーです。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content