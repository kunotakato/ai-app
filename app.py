import streamlit as st

from services.history_manager import init_db
from services.company_manager import init_company_tables

from app_pages.home_page import render_home_page
from app_pages.career_map_page import render_career_map_page
from app_pages.self_analysis_page import render_self_analysis_page
from app_pages.job_analysis_page import render_job_analysis_page
from app_pages.resume_page import render_resume_page
from app_pages.interview_page import render_interview_page
from app_pages.company_page import render_company_page
from app_pages.history_page import render_history_page


# ----------------------------------
# Streamlit基本設定
# ----------------------------------

st.set_page_config(
    page_title="CareerCraft AI",
    page_icon="📄",
    layout="wide",
)


# ----------------------------------
# データベース初期化
# ----------------------------------

init_db()
init_company_tables()


# ----------------------------------
# アプリタイトル
# ----------------------------------

st.title("📄 CareerCraft AI")

st.caption(
    "自己分析から応募・面接までを支援するAI就活・転職アプリ"
)


# ----------------------------------
# サイドバー
# ----------------------------------

with st.sidebar:

    page = st.radio(
        "ページ切り替え",
        [
            "はじめに",
            "マイ転職",
            "キャリア地図",
            "自己分析・職種診断",
            "求人分析",
            "職務経歴書作成",
            "面接対策",
            "生成履歴",
        ],
    )

    st.divider()

    st.header("使い方")

    st.markdown(
        """
        **初めて使う場合**

        1. キャリア地図
        2. 自己分析
        3. マイ転職へ企業登録
        4. 求人分析
        5. 職務経歴書
        6. 面接対策

        の順番がおすすめです。
        """
    )

    st.divider()

    st.warning(
        """
        氏名・住所・電話番号・顧客情報・
        社外秘情報などは入力しないでください。
        """
    )


# ----------------------------------
# ページ表示
# ----------------------------------

if page == "はじめに":

    render_home_page()


elif page == "マイ転職":

    render_company_page()


elif page == "キャリア地図":

    render_career_map_page()


elif page == "自己分析・職種診断":

    render_self_analysis_page()


elif page == "求人分析":

    render_job_analysis_page()


elif page == "職務経歴書作成":

    render_resume_page()


elif page == "面接対策":

    render_interview_page()


elif page == "生成履歴":

    render_history_page()