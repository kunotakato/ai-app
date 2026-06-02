import streamlit as st

from services.history_manager import init_db

from pages.resume_page import render_resume_page
from pages.job_analysis_page import render_job_analysis_page
from pages.self_analysis_page import render_self_analysis_page
from pages.history_page import render_history_page


st.set_page_config(
    page_title="CareerCraft AI",
    page_icon="📄",
    layout="wide",
)

init_db()

st.title("📄 CareerCraft AI")
st.caption("職務経歴書を“伝わる文章”に変えるAI転職支援ツール")


with st.sidebar:
    page = st.radio(
        "ページ切り替え",
        [
            "職務経歴書作成",
            "求人分析",
            "自己分析・職種診断",
            "生成履歴",
        ],
    )

    st.divider()

    st.header("使い方")
    st.write(
        """
        1. 基本情報を入力  
        2. 必要なら自己分析  
        3. 求人票を文章 or スクショで入力  
        4. 求人分析  
        5. 職務経歴書を生成  
        6. 履歴で再確認
        """
    )

    st.warning(
        """
        個人情報・会社の機密情報は入力しすぎないでください。

        入力を避けた方がよい例：
        - 氏名
        - 住所
        - 電話番号
        - 顧客名
        - 社外秘情報
        """
    )


if page == "職務経歴書作成":
    render_resume_page()

elif page == "求人分析":
    render_job_analysis_page()

elif page == "自己分析・職種診断":
    render_self_analysis_page()

elif page == "生成履歴":
    render_history_page()