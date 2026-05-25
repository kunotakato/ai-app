import os
import csv
from datetime import datetime


def ensure_directories():
    """
    必要なフォルダが存在しない場合に作成します。
    """
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("data", exist_ok=True)


def save_markdown(content):
    """
    生成した職務経歴書をMarkdownファイルとして保存します。
    """

    ensure_directories()

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"outputs/resume_{now}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def save_history(current_job, experience_years, target_job):
    """
    入力履歴をCSVに保存します。
    """

    ensure_directories()

    file_path = "data/history.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(
                [
                    "created_at",
                    "current_job",
                    "experience_years",
                    "target_job",
                ]
            )

        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                current_job,
                experience_years,
                target_job,
            ]
        )