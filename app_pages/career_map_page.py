import streamlit as st

from prompts.career_map_prompt import build_career_map_prompt
from services.career_map_generator import generate_career_map
from services.history_manager import save_generation_history


def load_career_map_sample():
    """
    医療職からAI/ITエンジニアを目指す人向けのサンプルです。
    """

    st.session_state.career_current_status = """医療職として働きながら、PythonやAIアプリ開発を学習しています。
現在は、医療現場で感じた非効率な業務をAIやシステムで改善できる人材を目指しています。"""

    st.session_state.career_reason_for_change = """夜勤や現場業務だけに将来を依存することに不安があります。
また、医療現場には在庫管理、記録、申し送り、データ確認などアナログな作業が多く、ITやAIで改善できる余地があると感じたためです。"""

    st.session_state.career_past_experience = """・透析業務で患者状態や血液データを確認してきた
・医療物品や薬剤の在庫確認を担当した
・Excelで管理表を作った
・Python、Streamlit、OpenAI APIを学習してアプリを作っている
・職務経歴書AIや在庫管理アプリの開発に取り組んでいる"""

    st.session_state.career_worries = """・未経験からエンジニアになれるか不安
・医療職の経験がIT転職で評価されるか不安
・どの職種を目指すべきか迷っている
・ポートフォリオの見せ方が分からない"""

    st.session_state.career_ideal_work_style = """・AIやデータ分析を使って課題解決したい
・現場改善に関わりたい
・学習しながら成長できる環境で働きたい
・将来的には自分で価値あるシステムを作れる人材になりたい"""


def render_career_map_page():
    """
    キャリア地図ページです。
    """

    st.subheader("🗺️ キャリア地図")
    st.caption("現在地・経験・不安・理想から、転職活動の方向性を整理します。")

    if st.button("医療職 → AI/ITエンジニア サンプルを入れる"):
        load_career_map_sample()
        st.success("キャリア地図サンプルを反映しました。")

    st.divider()

    current_status = st.text_area(
        "今のキャリア現在地",
        height=120,
        placeholder="例：現在は医療職として働きながら、PythonやAIを学習しています。",
        key="career_current_status",
    )

    reason_for_change = st.text_area(
        "転職理由・変えたい理由",
        height=120,
        placeholder="例：今の働き方に不安があり、ITやAIを使って課題解決できる仕事に挑戦したいです。",
        key="career_reason_for_change",
    )

    past_experience = st.text_area(
        "過去の経験",
        height=160,
        placeholder="例：これまで担当してきた業務、工夫したこと、学習していること、作ったものなど",
        key="career_past_experience",
    )

    worries = st.text_area(
        "今の不安",
        height=120,
        placeholder="例：未経験転職ができるか不安、自分に合う職種が分からない、面接で何を話せばいいか不安",
        key="career_worries",
    )

    ideal_work_style = st.text_area(
        "理想の働き方",
        height=120,
        placeholder="例：学習しながら成長したい、業務改善に関わりたい、AIを使って価値を作りたい",
        key="career_ideal_work_style",
    )

    st.info(
        """
        キャリア地図は、転職活動の最初に方向性を整理するための機能です。
        診断結果は参考情報として使い、最終判断は自分の希望や求人内容と合わせて考えてください。
        """
    )

    if st.button("キャリア地図を作成する", type="primary"):
        if not current_status or not past_experience:
            st.error("今のキャリア現在地と過去の経験を入力してください。")

        else:
            try:
                with st.spinner("キャリア地図を作成しています..."):
                    prompt = build_career_map_prompt(
                        current_status=current_status,
                        reason_for_change=reason_for_change,
                        past_experience=past_experience,
                        worries=worries,
                        ideal_work_style=ideal_work_style,
                    )

                    result = generate_career_map(prompt)

                    save_generation_history(
                        history_type="career_map",
                        current_job=current_status[:50],
                        target_job="",
                        input_summary="キャリア地図",
                        result=result,
                    )

                st.success("キャリア地図が完成しました！")

                st.subheader("キャリア地図結果")
                st.markdown(result)

                st.text_area(
                    "コピー用",
                    value=result,
                    height=420,
                )

                st.download_button(
                    label="Markdownでダウンロード",
                    data=result,
                    file_name="career_map.md",
                    mime="text/markdown",
                )

            except ValueError as e:
                st.error(str(e))

            except Exception as e:
                st.error("キャリア地図の作成中にエラーが発生しました。")
                st.code(str(e))