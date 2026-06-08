import streamlit as st

from prompts.interview_prompt import build_interview_prompt
from services.interview_generator import generate_interview_prep
from services.history_manager import save_generation_history

from app_pages.common import 
    (init_session_state
    render_sample_buttons,
    render_job_posting_inputs,
)


def load_interview_sample():
    """
    医療職からAI/ITエンジニア転職を想定した面接対策サンプルです。
    """

    st.session_state.interview_target_job = "AIエンジニア / データ分析エンジニア"

    st.session_state.interview_job_posting = """未経験歓迎のAIエンジニア / データ分析エンジニア募集。
Pythonを用いたデータ分析、業務効率化ツール開発、AIを活用した社内システム開発に関心がある方。

歓迎スキル：
Python、SQL、Git、Streamlit、機械学習の基礎、業務改善経験。

求める人物像：
自ら課題を見つけ、学習しながら改善提案できる方。
チームで協力しながら、ユーザー目線でシステム開発に取り組める方。"""

    st.session_state.interview_career_summary = """医療職として透析治療に関わり、患者状態の観察、血圧・体重・血液データの確認、医療物品や薬剤の在庫管理、申し送りや記録業務を担当してきました。
現場でアナログな業務や非効率な作業を経験し、Python、Streamlit、pandas、SQLite、OpenAI APIを学習しながら、在庫管理システムや職務経歴書AIなどのアプリ開発に取り組んでいます。
医療現場で培った正確性、観察力、課題発見力を活かし、AIやデータ分析を使って現場課題を解決できるエンジニアを目指しています。"""

    st.session_state.interview_concerns = """・未経験であることをどう説明すればいいか
・医療職の経験をエンジニアにどう活かせるか
・なぜエンジニアになりたいのかをうまく話せるか
・制作物について深掘りされたときに答えられるか"""


def render_interview_page():
    """
    面接対策ページです。
    """

    init_session_state()

    st.subheader("面接対策AI")
    st.caption("求人票・経歴・不安な質問から、面接想定質問と回答例を作成します。")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("医療職 → AI/ITエンジニア 面接サンプル"):
            load_interview_sample()
            st.success("面接対策サンプルを反映しました。")

    with col2:
        render_sample_buttons()

    st.divider()

    target_job = st.text_input(
        "応募職種",
        placeholder="例：AIエンジニア、データ分析エンジニア、Webマーケター",
        key="interview_target_job",
    )

    st.subheader("求人票")

    manual_job_posting = st.text_area(
        "求人票を文章で貼り付ける",
        height=180,
        placeholder="仕事内容、必須スキル、歓迎スキル、求める人物像などを貼り付けてください。",
        key="interview_job_posting",
    )

    st.caption("スクショから読み取る場合はこちらも使えます。")
    extracted_job_posting = render_job_posting_inputs()

    job_posting = manual_job_posting

    if extracted_job_posting:
        job_posting = manual_job_posting + "\n\n" + extracted_job_posting

    st.subheader("自分の経歴")

    career_summary = st.text_area(
        "自分の経歴・経験・制作物",
        height=220,
        placeholder="例：これまでの職務経験、学習中のスキル、制作物、転職理由などを入力してください。",
        key="interview_career_summary",
    )

    concerns = st.text_area(
        "不安な質問",
        height=140,
        placeholder="例：未経験であること、転職理由、前職経験の活かし方、制作物の深掘りなど",
        key="interview_concerns",
    )

    st.info(
        """
        面接回答は丸暗記ではなく、話す内容の整理として使ってください。
        実際の面接では、自分の言葉に直して話すことが大切です。
        """
    )

    if st.button("面接対策を生成する", type="primary"):
        if not target_job:
            st.error("応募職種を入力してください。")

        elif not career_summary:
            st.error("自分の経歴を入力してください。")

        else:
            try:
                with st.spinner("面接対策を作成しています..."):
                    prompt = build_interview_prompt(
                        target_job=target_job,
                        job_posting=job_posting,
                        career_summary=career_summary,
                        concerns=concerns,
                    )

                    result = generate_interview_prep(prompt)

                    save_generation_history(
                        history_type="面接対策",
                        current_job="",
                        target_job=target_job,
                        input_summary=f"{target_job} の面接対策",
                        result=result,
                    )

                st.success("面接対策が完成しました！")

                st.subheader("面接対策結果")
                st.markdown(result)

                st.text_area(
                    "面接対策コピー用",
                    value=result,
                    height=420,
                )

                st.download_button(
                    label="Markdownでダウンロード",
                    data=result,
                    file_name="interview_prep.md",
                    mime="text/markdown",
                )

            except ValueError as e:
                st.error(str(e))

            except Exception as e:
                st.error("面接対策生成中にエラーが発生しました。")
                st.code(str(e))