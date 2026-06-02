import os
import sqlite3
from datetime import datetime

DB_PATH = "database/career_craft.db"


def init_db():
    """
    SQLiteデータベースと履歴テーブルを自動作成します。
    """
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS generation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            type TEXT NOT NULL,
            current_job TEXT,
            target_job TEXT,
            input_summary TEXT,
            result TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def save_generation_history(
    history_type: str,
    current_job: str,
    target_job: str,
    input_summary: str,
    result: str,
):
    """
    生成結果をSQLiteに保存します。
    """

    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO generation_history (
            created_at,
            type,
            current_job,
            target_job,
            input_summary,
            result
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            history_type,
            current_job,
            target_job,
            input_summary,
            result,
        ),
    )

    conn.commit()
    conn.close()


def get_generation_history():
    """
    保存済みの生成履歴を新しい順で取得します。
    """

    init_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            created_at,
            type,
            current_job,
            target_job,
            input_summary,
            result
        FROM generation_history
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_generation_history_by_id(history_id: int):
    """
    IDを指定して1件の履歴を取得します。
    """

    init_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            created_at,
            type,
            current_job,
            target_job,
            input_summary,
            result
        FROM generation_history
        WHERE id = ?
        """,
        (history_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return dict(row)


def delete_generation_history(history_id: int):
    """
    IDを指定して履歴を削除します。
    """

    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM generation_history
        WHERE id = ?
        """,
        (history_id,),
    )

    conn.commit()
    conn.close()