import streamlit as st

from prompts.resume_prompt import build_resume_prompt
from services.openai_client import generate_resume
from services.file_storage import save_markdown, save_history


st.set_page_config(
    page_title="CareerCraft AI",
    page_icon="📄",
    layout="wide",
)


st.title("📄 CareerCraft AI")
st.caption("職務経歴書を“伝わる文章”に変えるAIツール")


with st.sidebar:
    st.header("使い方")
    st.write(
        """
        1. 必要項目を入力  
        2. 生成ボタンを押す  
        3. AIが職務経歴書の下書きを作成  
        4. Markdownで保存できます
        """
    )

    st.warning(
        "個人情報や会社の機密情報は入力しすぎないようにしてください。"
    )


st.subheader("基本情報を入力してください")

col1, col2 = st.columns(2)

with col1:
    current_job = st.text_input(
        "現在の職種",
        placeholder="例：営業職、事務職、看護師、販売職、エンジニア",
    )

with col2:
    experience_years = st.text_input(
        "経験年数",
        placeholder="例：3年",
    )

target_job = st.text_input(
    "転職希望職種",
    placeholder="例：Webマーケター、事務職、AIエンジニア、営業職",
)

tone = st.selectbox(
    "文章のトーン",
    [
        "誠実で自然な転職書類向け",
        "実績をしっかりアピールする",
        "未経験転職向けにポテンシャルを伝える",
        "落ち着いたビジネス文書風",
    ],
)

st.subheader("これまでの経験を入力してください")

work_details = st.text_area(
    "これまでの業務内容",
    height=160,
    placeholder="例：\n・既存顧客への提案営業\n・見積書、提案資料の作成\n・売上管理\n・新人教育",
)

achievements = st.text_area(
    "実績・工夫したこと",
    height=160,
    placeholder="例：\n・月間売上120%達成\n・業務マニュアルを作成\n・問い合わせ対応時間を短縮",
)

strengths = st.text_area(
    "自分の強み",
    height=120,
    placeholder="例：\n・相手の課題を聞き出す力\n・継続力\n・分かりやすく説明する力",
)


st.divider()

if st.button("職務経歴書を生成する", type="primary"):
    if not current_job or not experience_years or not target_job:
        st.error(
            "基本情報が不足しています。現在の職種・経験年数・転職希望職種を入力してください。"
        )

    elif not work_details:
        st.error(
            "業務内容が入力されていません。箇条書きで大丈夫なので入力してください。"
        )

    else:
        try:
            with st.spinner("AIが職務経歴書を作成しています..."):
                prompt = build_resume_prompt(
                    current_job=current_job,
                    experience_years=experience_years,
                    target_job=target_job,
                    work_details=work_details,
                    achievements=achievements,
                    strengths=strengths,
                    tone=tone,
                )

                result = generate_resume(prompt)

                save_history(
                    current_job=current_job,
                    experience_years=experience_years,
                    target_job=target_job,
                )

                file_path = save_markdown(result)

            st.success("職務経歴書の下書きが完成しました！")

            st.subheader("生成結果")
            st.markdown(result)

            st.download_button(
                label="Markdownファイルをダウンロード",
                data=result,
                file_name="career_resume.md",
                mime="text/markdown",
            )

            st.info(f"保存先：{file_path}")

        except ValueError as e:
            st.error(str(e))

        except Exception as e:
            st.error("エラーが発生しました。入力内容やAPIキーを確認してください。")
            st.code(str(e))