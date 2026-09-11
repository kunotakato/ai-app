import sqlite3
from datetime import datetime

from services.history_manager import DB_PATH


# 選考状況として使用する値です。
COMPANY_STATUSES = [
    "検討中",
    "応募予定",
    "応募済み",
    "書類選考中",
    "一次面接",
    "二次面接",
    "最終面接",
    "内定",
    "不採用",
    "辞退",
]


def get_connection():
    """
    SQLiteへ接続します。

    foreign_keys = ON にすることで、
    企業削除時に紐付いたデータも削除できるようにします。
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def init_company_tables():
    """
    応募企業管理用のテーブルを作成します。

    すでに存在する場合は何もしないので、
    アプリ起動時に毎回実行して問題ありません。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            job_title TEXT,
            job_url TEXT,
            job_posting TEXT,
            status TEXT NOT NULL DEFAULT '検討中',
            priority INTEGER NOT NULL DEFAULT 3,
            memo TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS company_artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            title TEXT,
            result TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (company_id)
                REFERENCES companies(id)
                ON DELETE CASCADE
        )
        """
    )

    conn.commit()
    conn.close()


def create_company(
    company_name: str,
    job_title: str = "",
    job_url: str = "",
    job_posting: str = "",
    status: str = "検討中",
    priority: int = 3,
    memo: str = "",
):
    """
    応募企業を新規登録します。

    戻り値：
        作成した企業のID
    """

    init_company_tables()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO companies (
            company_name,
            job_title,
            job_url,
            job_posting,
            status,
            priority,
            memo,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            company_name.strip(),
            job_title.strip(),
            job_url.strip(),
            job_posting.strip(),
            status,
            priority,
            memo.strip(),
            now,
            now,
        ),
    )

    company_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return company_id


def get_companies():
    """
    応募企業を新しい順に取得します。
    """

    init_company_tables()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM companies
        ORDER BY updated_at DESC, id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_company_by_id(company_id: int):
    """
    企業IDを指定して1件取得します。
    """

    init_company_tables()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        (company_id,),
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


def update_company(
    company_id: int,
    company_name: str,
    job_title: str,
    job_url: str,
    job_posting: str,
    status: str,
    priority: int,
    memo: str,
):
    """
    応募企業の情報を更新します。
    """

    init_company_tables()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE companies
        SET
            company_name = ?,
            job_title = ?,
            job_url = ?,
            job_posting = ?,
            status = ?,
            priority = ?,
            memo = ?,
            updated_at = ?
        WHERE id = ?
        """,
        (
            company_name.strip(),
            job_title.strip(),
            job_url.strip(),
            job_posting.strip(),
            status,
            priority,
            memo.strip(),
            now,
            company_id,
        ),
    )

    conn.commit()
    conn.close()


def delete_company(company_id: int):
    """
    応募企業を削除します。

    ON DELETE CASCADEにより、
    company_artifactsにある関連データも削除されます。
    """

    init_company_tables()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM companies
        WHERE id = ?
        """,
        (company_id,),
    )

    conn.commit()
    conn.close()


def save_company_artifact(
    company_id: int,
    artifact_type: str,
    result: str,
    title: str = "",
):
    """
    AI生成結果を特定企業へ紐付けて保存します。

    Phase6-2以降で、
    求人分析・職務経歴書・面接対策などから利用します。
    """

    init_company_tables()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO company_artifacts (
            company_id,
            type,
            title,
            result,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            company_id,
            artifact_type,
            title.strip(),
            result,
            now,
        ),
    )

    conn.commit()
    conn.close()


def get_company_artifacts(company_id: int):
    """
    指定企業に紐付いているAI生成結果を取得します。
    """

    init_company_tables()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM company_artifacts
        WHERE company_id = ?
        ORDER BY created_at DESC, id DESC
        """,
        (company_id,),
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]