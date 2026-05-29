import re
import streamlit as st

from prompts.resume_prompt import build_resume_prompt
from prompts.job_analysis_prompt import build_job_analysis_prompt
from services.openai_client import generate_resume
from services.file_storage import save_markdown, save_history
from services.vision_parser import extract_job_posting_from_image
from services.document_exporter import export_to_docx, export_to_pdf
from services.job_analyzer import analyze_job_match


st.set_page_config(
    page_title="CareerCraft AI",
    page_icon="📄",
    layout="wide",
)


st.title("📄 CareerCraft AI")
st.caption("職務経歴書を“伝わる文章”に変えるAIツール")


if "extracted_job_posting" not in st.session_state:
    st.session_state.extracted_job_posting = ""

if "job_analysis_result" not in st.session_state:
    st.session_state.job_analysis_result = ""


def extract_section(content: str, heading: str) -> str:
    """
    AI生成結果から、指定した見出し部分だけを抜き出します。
    見出しが見つからない場合は空文字を返します。
    """

    pattern = rf"## .*{re.escape(heading)}.*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(1).strip()

    return ""


def extract_match_rate(analysis_text: str) -> str:
    """
    求人分析結果から「マッチ率：〇〇%」を抜き出します。
    見つからない場合は空文字を返します。
    """

    match = re.search(r"マッチ率[:：]\s*(\d{1,3})\s*%", analysis_text)

    if match:
        return match.group(1)

    return ""


def load_sales_sample():
    st.session_state.current_job = "営業職"
    st.session_state.experience_years = "3年"
    st.session_state.target_job = "Webマーケター"
    st.session_state.work_details = """・法人顧客への新規提案営業
・既存顧客へのフォロー対応
・見積書、提案資料の作成
・売上管理、顧客管理
・新人メンバーへの業務共有"""
    st.session_state.achievements = """・月間売上目標を120%達成
・顧客管理表を改善し、対応漏れを削減
・新人向けの営業トークマニュアルを作成
・既存顧客からの追加受注を獲得"""
    st.session_state.strengths = """・相手の課題を聞き出す力
・分かりやすく説明する力
・継続して改善する力
・数字を見ながら行動を修正する力"""
    st.session_state.career_change_mode = True
    st.session_state.current_industry = "営業"
    st.session_state.reason_for_change = "営業活動の中で、集客や顧客心理、データをもとにした改善に興味を持ち、Webマーケターとして事業成長に関わりたいと考えたため。"
    st.session_state.transferable_experience = """・顧客課題を聞き出す力
・提案内容を分かりやすく伝える力
・数字をもとに行動を改善する力
・顧客目線で考える力"""
    st.session_state.learning_skills = "SEO、SNS運用、広告運用、Google Analytics、ライティング"
    st.session_state.portfolio = "SNS投稿分析、簡易LP作成、ブログ記事作成などに取り組んでいます。"
    st.session_state.job_posting_input = ""
    st.session_state.extracted_job_posting = ""
    st.session_state.job_analysis_result = ""


def load_medical_engineer_sample():
    st.session_state.current_job = "医療職"
    st.session_state.experience_years = "5年"
    st.session_state.target_job = "AIエンジニア / データ分析エンジニア"
    st.session_state.work_details = """・透析治療に関する装置準備、患者対応、治療中の状態観察
・血圧、体重、血液データなどを確認し、治療条件の判断をサポート
・医療物品や薬剤の在庫確認、発注管理
・申し送りや記録業務を通じた情報共有
・業務改善のためのExcel管理表やデータ整理の実施"""
    st.session_state.achievements = """・在庫管理の見直しにより確認作業の負担を軽減
・血圧低下や血液データの変化に注目し、治療中のリスク把握に努めた
・PythonやStreamlitを学習し、在庫管理やデータ分析アプリの開発に取り組んだ
・現場の非効率な作業をシステムで改善できないか継続的に検討した"""
    st.session_state.strengths = """・現場課題を見つける力
・正確に記録、確認する力
・データから状態変化を読み取る力
・多職種と連携するコミュニケーション力
・業務改善への関心と学習継続力"""
    st.session_state.career_change_mode = True
    st.session_state.current_industry = "医療"
    st.session_state.reason_for_change = """医療現場で働く中で、在庫管理や申し送り、データ確認など、まだアナログで非効率な業務が多いことを実感しました。
その経験から、ITやAIを活用して現場課題を解決できるエンジニアを目指したいと考えるようになりました。"""
    st.session_state.transferable_experience = """・患者状態の変化に気づく観察力
・血圧や血液データなどを確認する習慣
・ミスを防ぐ正確性
・多職種と連携する力
・現場業務の非効率を見つける課題発見力
・医療物品や薬剤の在庫管理経験"""
    st.session_state.learning_skills = """・Python
・Streamlit
・pandas
・SQLite
・OpenAI API
・Git / GitHub
・データ分析
・機械学習の基礎"""
    st.session_state.portfolio = """・職務経歴書AIツール CareerCraft AI
・在庫管理システム
・TOEIC学習サポートアプリ
・半導体工場向け異常検知AIダッシュボード
・SNS投稿生成、分析ツール"""
    st.session_state.job_posting_input = ""
    st.session_state.extracted_job_posting = ""
    st.session_state.job_analysis_result = ""


with st.sidebar:
    st.header("使い方")
    st.write(
        """
        1. 必要項目を入力  
        2. 求人票を文章 or スクショで入力  
        3. 求人との相性を分析  
        4. 職務経歴書の下書きを作成  
        5. Markdown / Word / PDFで保存
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


st.subheader("サンプル入力")

col_sample1, col_sample2 = st.columns(2)

with col_sample1:
    if st.button("営業職 → Webマーケター サンプル"):
        load_sales_sample()
        st.success("営業職サンプルを反映しました。")

with col_sample2:
    if st.button("医療職 → AI/ITエンジニア サンプル"):
        load_medical_engineer_sample()
        st.success("医療職→エンジニア転職サンプルを反映しました。")


st.divider()

st.subheader("基本情報")

col1, col2 = st.columns(2)

with col1:
    current_job = st.text_input(
        "現在の職種",
        placeholder="例：営業職、事務職、看護師、販売職、エンジニア",
        key="current_job",
    )

with col2:
    experience_years = st.text_input(
        "経験年数",
        placeholder="例：3年",
        key="experience_years",
    )

target_job = st.text_input(
    "転職希望職種",
    placeholder="例：Webマーケター、事務職、AIエンジニア、営業職",
    key="target_job",
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


st.subheader("これまでの経験")

work_details = st.text_area(
    "これまでの業務内容",
    height=160,
    placeholder="例：\n・既存顧客への提案営業\n・見積書、提案資料の作成\n・売上管理",
    key="work_details",
)

achievements = st.text_area(
    "実績・工夫したこと",
    height=160,
    placeholder="例：\n・月間売上120%達成\n・業務マニュアルを作成",
    key="achievements",
)

strengths = st.text_area(
    "自分の強み",
    height=120,
    placeholder="例：\n・課題発見力\n・継続力\n・分かりやすく説明する力",
    key="strengths",
)


st.subheader("未経験転職モード")

career_change_mode = st.checkbox(
    "未経験職種への転職として作成する",
    value=False,
    key="career_change_mode",
)

current_industry = ""
reason_for_change = ""
transferable_experience = ""
learning_skills = ""
portfolio = ""

if career_change_mode:
    st.info("現在の経験を、転職希望職種で評価される言葉に変換します。")

    current_industry = st.text_input(
        "現在の業界",
        placeholder="例：医療、介護、営業、販売、事務",
        key="current_industry",
    )

    reason_for_change = st.text_area(
        "転職したい理由",
        height=100,
        placeholder="例：現場課題をITやAIで解決したいと考えたため。",
        key="reason_for_change",
    )

    transferable_experience = st.text_area(
        "転職先で活かしたい経験",
        height=120,
        placeholder="例：\n・課題発見力\n・正確な記録力\n・多職種連携",
        key="transferable_experience",
    )

    learning_skills = st.text_area(
        "学習中のスキル",
        height=100,
        placeholder="例：\n・Python\n・Streamlit\n・Git / GitHub\n・SQL",
        key="learning_skills",
    )

    portfolio = st.text_area(
        "制作物・ポートフォリオ",
        height=120,
        placeholder="例：\n・在庫管理アプリ\n・AIチャットボット\n・データ分析ダッシュボード",
        key="portfolio",
    )


st.subheader("求人票入力")

job_posting_input = st.text_area(
    "求人票を文章で貼り付ける",
    height=180,
    placeholder="求人票の仕事内容、必須スキル、歓迎スキル、求める人物像などを貼り付けてください。",
    key="job_posting_input",
)

uploaded_image = st.file_uploader(
    "求人票スクショをアップロード",
    type=["png", "jpg", "jpeg"],
)

if uploaded_image is not None:
    st.image(
        uploaded_image,
        caption="アップロードされた求人票スクショ",
        use_container_width=True,
    )

    if st.button("スクショから求人票を読み取る"):
        try:
            with st.spinner("求人票スクショを読み取っています..."):
                extracted_job_text = extract_job_posting_from_image(uploaded_image)

            st.session_state.extracted_job_posting = extracted_job_text
            st.success("求人票スクショの読み取りが完了しました。")

        except ValueError as e:
            st.error(str(e))

        except Exception as e:
            st.error("求人票スクショの読み取り中にエラーが発生しました。")
            st.code(str(e))


if st.session_state.extracted_job_posting:
    st.subheader("スクショから読み取った求人票")

    st.text_area(
        "読み取り結果",
        value=st.session_state.extracted_job_posting,
        height=240,
        key="extracted_job_posting_display",
    )

    if st.button("読み取り結果をクリア"):
        st.session_state.extracted_job_posting = ""
        st.session_state.job_analysis_result = ""
        st.rerun()


job_posting = job_posting_input

if st.session_state.extracted_job_posting:
    job_posting = job_posting_input + "\n\n" + st.session_state.extracted_job_posting


st.info(
    """
    求人票を文章またはスクショで入力すると、AIが求人内容に合わせて職務経歴書を調整します。
    空欄でも職務経歴書は生成できます。
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