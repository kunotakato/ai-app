from services.openai_client import get_openai_client


def generate_career_map(prompt: str) -> str:
    """
    OpenAI APIを使ってキャリア地図を生成します。
    """

    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "あなたは自己分析と転職支援に強いAIキャリアコーチです。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.6,
    )

    return response.choices[0].message.content