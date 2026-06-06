import streamlit as st

from services.history_manager import init_db

from pages.resume_page import render_resume_page
from pages.job_analysis_page import render_job_analysis_page
from pages.self_analysis_page import render_self_analysis_page
from pages.interview_page import render_interview_page
from pages.career_map_page import render_career_map_page
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
    st.write(
        """
        1. キャリア地図で現在地を整理  
        2. 自己分析で強みを言語化  
        3. 求人票を分析  
        4. 職務経歴書を生成  
        5. 面接対策を作成  
        6. 生成履歴で再確認
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


if page == "キャリア地図":
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