import streamlit as st

from prompts.self_analysis_prompt import build_self_analysis_prompt
from services.self_analyzer import analyze_self
from services.history_manager import save_generation_history

from app_pages.common import (
    init_session_state
    render_sample_buttons,
)


def render_self_analysis_page():
    """
    自己分析・職種診断ページです。
    """

    init_session_state()

    render_sample_buttons()

    st.divider()

    st.subheader("自己分析・職種診断")

    st.caption("得意・苦手・興味から、向いている職種や転職軸を整理します。")

    enjoyable_work = st.text_area(
        "楽しかった仕事・作業",
        height=100,
        placeholder="例：データを整理すること、業務改善を考えること、資料を分かりやすく作ること",
        key="enjoyable_work",
    )

    difficult_work = st.text_area(
        "苦手だった仕事・作業",
        height=100,
        placeholder="例：同じ作業の繰り返し、目的が曖昧な作業、感覚だけで進める仕事",
        key="difficult_work",
    )

    good_at = st.text_area(
        "得意だと思うこと",
        height=100,
        placeholder="例：整理すること、コツコツ続けること、人に説明すること",
        key="good_at",
    )

    praised_for = st.text_area(
        "人から褒められたこと",
        height=100,
        placeholder="例：丁寧、分かりやすい、責任感がある、改善案を出せる",
        key="praised_for",
    )

    avoid_work_style = st.text_area(
        "避けたい働き方",
        height=100,
        placeholder="例：長時間労働、教育体制がない、根性論が強い、改善提案しづらい環境",
        key="avoid_work_style",
    )

    interests = st.text_area(
        "興味のある分野",
        height=100,
        placeholder="例：AI、データ分析、Webマーケ、医療DX、業務改善",
        key="interests",
    )

    self_learning_skills = st.text_area(
        "学習中のスキル",
        height=100,
        placeholder="例：Python、Streamlit、SQL、Git、データ分析",
        key="self_learning_skills",
    )

    future_goal = st.text_area(
        "将来どうなりたいか",
        height=100,
        placeholder="例：AIやデータを使って現場課題を解決できる人材になりたい",
        key="future_goal",
    )

    if st.button("自己分析する"):
        if not enjoyable_work and not good_at and not interests:
            st.error("自己分析に必要な情報が不足しています。楽しかった作業・得意なこと・興味のある分野のいずれかを入力してください。")

        else:
            try:
                with st.spinner("自己分析・職種診断を実行しています..."):
                    self_prompt = build_self_analysis_prompt(
                        enjoyable_work=enjoyable_work,
                        difficult_work=difficult_work,
                        good_at=good_at,
                        praised_for=praised_for,
                        avoid_work_style=avoid_work_style,
                        interests=interests,
                        learning_skills=self_learning_skills,
                        future_goal=future_goal,
                    )

                    self_result = analyze_self(self_prompt)
                    st.session_state.self_analysis_result = self_result

                    save_generation_history(
                        history_type="自己分析",
                        current_job=st.session_state.get("current_job", ""),
                        target_job=st.session_state.get("target_job", ""),
                        input_summary="自己分析・職種診断",
                        result=self_result,
                    )

                st.success("自己分析が完了しました。")

            except ValueError as e:
                st.error(str(e))

            except Exception as e:
                st.error("自己分析中にエラーが発生しました。")
                st.code(str(e))

    if st.session_state.self_analysis_result:
        st.subheader("自己分析結果")
        st.warning("診断結果はAIによる参考情報です。可能性を狭めすぎず、転職活動の整理材料として使ってください。")
        st.markdown(st.session_state.self_analysis_result)

        st.text_area(
            "自己分析結果コピー用",
            value=st.session_state.self_analysis_result,
            height=360,
        )

        if st.button("自己分析結果をクリア"):
            st.session_state.self_analysis_result = ""
            st.rerun()