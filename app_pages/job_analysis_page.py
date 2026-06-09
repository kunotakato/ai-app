import streamlit as st

from prompts.job_analysis_prompt import build_job_analysis_prompt
from services.job_analyzer import analyze_job_match
from services.history_manager import save_generation_history

from app_pages.common import (
    init_session_state,
    render_sample_buttons,
    render_basic_inputs,
    render_experience_inputs,
    render_career_change_inputs,
    render_job_posting_inputs,
    extract_match_rate,
)


def render_job_analysis_page():
    """
    求人分析ページです。
    """

    init_session_state()

    render_sample_buttons()

    st.divider()

    current_job, experience_years, target_job, _tone = render_basic_inputs()

    work_details, achievements, strengths = render_experience_inputs()

    (
        _career_change_mode,
        _current_industry,
        _reason_for_change,
        _transferable_experience,
        learning_skills,
        portfolio,
    ) = render_career_change_inputs()

    st.divider()

    job_posting = render_job_posting_inputs()

    st.info(
        """
        求人票を文章またはスクショで入力すると、AIが求人内容を分析します。
        """
    )

    st.divider()

    st.subheader("求人分析")

    st.caption("求人票とあなたの経験を照らし合わせて、相性・不足スキル・強調ポイントを分析します。")

    if st.button("求人との相性を分析する"):
        if not job_posting.strip():
            st.error("求人票を入力してください。文章で貼り付けるか、スクショから読み取ってください。")

        elif not current_job or not target_job:
            st.error("現在の職種と転職希望職種を入力してください。")

        else:
            try:
                with st.spinner("求人との相性を分析しています..."):
                    analysis_prompt = build_job_analysis_prompt(
                        current_job=current_job,
                        experience_years=experience_years,
                        target_job=target_job,
                        work_details=work_details,
                        achievements=achievements,
                        strengths=strengths,
                        learning_skills=learning_skills,
                        portfolio=portfolio,
                        job_posting=job_posting,
                    )

                    analysis_result = analyze_job_match(analysis_prompt)
                    st.session_state.job_analysis_result = analysis_result

                    save_generation_history(
                        history_type="求人分析",
                        current_job=current_job,
                        target_job=target_job,
                        input_summary=f"{current_job} → {target_job} の求人分析",
                        result=analysis_result,
                    )

                st.success("求人分析が完了しました。")

            except ValueError as e:
                st.error(str(e))

            except Exception as e:
                st.error("求人分析中にエラーが発生しました。")
                st.code(str(e))

    if st.session_state.job_analysis_result:
        st.subheader("求人分析結果")

        match_rate = extract_match_rate(st.session_state.job_analysis_result)

        if match_rate:
            st.metric(
                label="求人とのマッチ率",
                value=f"{match_rate}%",
            )

        st.warning("マッチ率はAIによる目安です。合否や市場価値を保証するものではありません。")
        st.markdown(st.session_state.job_analysis_result)

        st.text_area(
            "求人分析結果コピー用",
            value=st.session_state.job_analysis_result,
            height=320,
        )

        if st.button("求人分析結果をクリア"):
            st.session_state.job_analysis_result = ""
            st.rerun()