import streamlit as st

from prompts.resume_prompt import build_resume_prompt
from services.openai_client import generate_resume
from services.file_storage import save_markdown, save_history
from services.document_exporter import export_to_docx, export_to_pdf
from services.history_manager import save_generation_history

from app_pages.common import init_session_state
    init_session_state,
    render_sample_buttons,
    render_basic_inputs,
    render_experience_inputs,
    render_career_change_inputs,
    render_job_posting_inputs,
    extract_section,
)


def render_resume_page():
    """
    職務経歴書作成ページです。
    """

    init_session_state()

    render_sample_buttons()

    st.divider()

    current_job, experience_years, target_job, tone = render_basic_inputs()

    work_details, achievements, strengths = render_experience_inputs()

    (
        career_change_mode,
        current_industry,
        reason_for_change,
        transferable_experience,
        learning_skills,
        portfolio,
    ) = render_career_change_inputs()

    st.divider()

    job_posting = render_job_posting_inputs()

    st.info(
        """
        求人票を文章またはスクショで入力すると、AIが求人内容に合わせて職務経歴書を調整します。
        空欄でも職務経歴書は生成できます。
        """
    )

    st.divider()

    st.info(
        """
        生成される文章は下書きです。
        実際に応募する前に、内容が事実と合っているか必ず確認してください。
        """
    )

    if st.button("職務経歴書を生成する", type="primary"):
        if not current_job or not experience_years or not target_job:
            st.error("基本情報が不足しています。現在の職種・経験年数・転職希望職種を入力してください。")

        elif not work_details:
            st.error("業務内容が入力されていません。箇条書きで大丈夫なので入力してください。")

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
                        career_change_mode=career_change_mode,
                        current_industry=current_industry,
                        reason_for_change=reason_for_change,
                        transferable_experience=transferable_experience,
                        learning_skills=learning_skills,
                        portfolio=portfolio,
                        job_posting=job_posting,
                    )

                    result = generate_resume(prompt)

                    save_generation_history(
                        history_type="職務経歴書",
                        current_job=current_job,
                        target_job=target_job,
                        input_summary=f"{current_job} → {target_job}",
                        result=result,
                    )

                    save_history(
                        current_job=current_job,
                        experience_years=experience_years,
                        target_job=target_job,
                    )

                    file_path = save_markdown(result)

                st.success("職務経歴書の下書きが完成しました！")

                st.subheader("生成結果")
                st.markdown(result)

                st.subheader("そのままコピー用")

                section_map = {
                    "職務要約": extract_section(result, "職務要約"),
                    "職務経歴": extract_section(result, "職務経歴"),
                    "活かせる経験・スキル": extract_section(result, "活かせる経験・スキル"),
                    "自己PR": extract_section(result, "自己PR"),
                    "志望動機": extract_section(result, "志望動機"),
                    "面接で話すポイント": extract_section(result, "面接で話すべきポイント"),
                }

                for label, text in section_map.items():
                    if text:
                        st.text_area(
                            label,
                            value=text,
                            height=180,
                        )

                st.text_area(
                    "全文コピー用",
                    value=result,
                    height=420,
                )

                docx_data = export_to_docx(result)
                pdf_data = export_to_pdf(result)

                col_dl1, col_dl2, col_dl3 = st.columns(3)

                with col_dl1:
                    st.download_button(
                        label="Markdownをダウンロード",
                        data=result,
                        file_name="career_resume.md",
                        mime="text/markdown",
                    )

                with col_dl2:
                    st.download_button(
                        label="Wordをダウンロード",
                        data=docx_data,
                        file_name="career_resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )

                with col_dl3:
                    st.download_button(
                        label="PDFをダウンロード",
                        data=pdf_data,
                        file_name="career_resume.pdf",
                        mime="application/pdf",
                    )

                st.info(f"保存先：{file_path}")

            except ValueError as e:
                st.error(str(e))

            except Exception as e:
                st.error("エラーが発生しました。入力内容やAPIキーを確認してください。")
                st.code(str(e))