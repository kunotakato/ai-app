from services.openai_client import get_openai_client


def analyze_job_match(prompt: str) -> str:
    """
    OpenAI APIを使って求人票とユーザー経験のマッチ度を分析します。
    """

    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "あなたは求人票分析と転職支援に強いキャリアアドバイザーです。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.4,
    )

    return response.choices[0].message.content