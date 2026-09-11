import streamlit as st

from services.company_manager import (
    COMPANY_STATUSES,
    create_company,
    delete_company,
    get_companies,
    get_company_artifacts,
    get_company_by_id,
    init_company_tables,
    update_company,
)


def priority_label(priority: int) -> str:
    """
    数字の志望度を★表示へ変換します。
    """

    return "★" * priority + "☆" * (5 - priority)


def render_company_page():
    """
    応募企業管理ページ全体を表示します。
    """

    init_company_tables()

    st.header("💼 マイ転職")
    st.caption(
        "気になる企業・応募企業・選考状況をまとめて管理します。"
    )

    st.info(
        """
        まず気になる企業を登録してください。

        今後この企業情報に、
        求人分析・職務経歴書・企業研究・面接対策を
        すべて紐付けていきます。
        """
    )

    tab1, tab2 = st.tabs(
        [
            "➕ 企業を登録",
            "🏢 応募企業一覧",
        ]
    )

    # -----------------------------
    # 新規企業登録
    # -----------------------------
    with tab1:
        render_company_create_form()

    # -----------------------------
    # 応募企業一覧
    # -----------------------------
    with tab2:
        render_company_list()


def render_company_create_form():
    """
    新規企業登録フォームを表示します。
    """

    st.subheader("応募企業を登録")

    with st.form("company_create_form"):

        company_name = st.text_input(
            "企業名 *",
            placeholder="例：株式会社〇〇",
        )

        job_title = st.text_input(
            "応募職種",
            placeholder="例：AIエンジニア",
        )

        job_url = st.text_input(
            "求人URL",
            placeholder="https://example.com/jobs/123",
        )

        status = st.selectbox(
            "現在の選考状況",
            COMPANY_STATUSES,
        )

        priority = st.slider(
            "志望度",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = 低い / 5 = 第一志望クラス",
        )

        job_posting = st.text_area(
            "求人票",
            height=180,
            placeholder=(
                "求人サイトの仕事内容・必須スキル・"
                "歓迎スキルなどを貼り付けてください。"
            ),
        )

        memo = st.text_area(
            "メモ",
            height=120,
            placeholder=(
                "例：\n"
                "・医療経験が活かせそう\n"
                "・教育制度を面接で確認したい\n"
                "・第一志望候補"
            ),
        )

        submitted = st.form_submit_button(
            "企業を登録する",
            type="primary",
        )

    if submitted:

        if not company_name.strip():
            st.error(
                "企業名が入力されていません。"
                "応募を検討している会社名を入力してください。"
            )

            return

        try:
            company_id = create_company(
                company_name=company_name,
                job_title=job_title,
                job_url=job_url,
                job_posting=job_posting,
                status=status,
                priority=priority,
                memo=memo,
            )

            st.success(
                f"「{company_name}」を登録しました！"
            )

            st.caption(
                f"企業ID：{company_id}"
            )

        except Exception as e:
            st.error(
                "企業の保存中に問題が発生しました。"
                "入力内容を確認して、もう一度試してください。"
            )

            st.code(str(e))


def render_company_list():
    """
    登録済み企業一覧を表示します。
    """

    companies = get_companies()

    if not companies:
        st.info(
            "まだ企業が登録されていません。"
            "「企業を登録」タブから最初の1社を登録してみましょう。"
        )

        return

    # -----------------------------
    # 状況の簡易サマリー
    # -----------------------------

    total = len(companies)

    active = len(
        [
            c
            for c in companies
            if c["status"]
            not in ["内定", "不採用", "辞退"]
        ]
    )

    offers = len(
        [
            c
            for c in companies
            if c["status"] == "内定"
        ]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "登録企業",
        total,
    )

    col2.metric(
        "選考中",
        active,
    )

    col3.metric(
        "内定",
        offers,
    )

    st.divider()

    # -----------------------------
    # フィルター
    # -----------------------------

    filter_status = st.selectbox(
        "選考状況で絞り込み",
        ["すべて"] + COMPANY_STATUSES,
    )

    filtered_companies = companies

    if filter_status != "すべて":
        filtered_companies = [
            company
            for company in companies
            if company["status"] == filter_status
        ]

    if not filtered_companies:
        st.info(
            "この条件に該当する企業はありません。"
        )

        return

    # -----------------------------
    # 企業選択
    # -----------------------------

    company_options = {
        (
            f"{company['company_name']}｜"
            f"{company['job_title'] or '職種未設定'}｜"
            f"{company['status']}"
        ): company["id"]
        for company in filtered_companies
    }

    selected_label = st.selectbox(
        "詳細を見る企業",
        list(company_options.keys()),
    )

    company_id = company_options[selected_label]

    render_company_detail(company_id)


def render_company_detail(company_id: int):
    """
    企業詳細画面を表示します。
    """

    company = get_company_by_id(company_id)

    if company is None:
        st.error(
            "企業情報が見つかりませんでした。"
        )

        return

    st.divider()

    st.subheader(
        f"🏢 {company['company_name']}"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "応募職種",
        company["job_title"] or "未設定",
    )

    col2.metric(
        "選考状況",
        company["status"],
    )

    col3.metric(
        "志望度",
        priority_label(company["priority"]),
    )

    if company["job_url"]:
        st.link_button(
            "求人ページを開く",
            company["job_url"],
        )

    st.caption(
        f"登録日：{company['created_at']} / "
        f"最終更新：{company['updated_at']}"
    )

    detail_tab, edit_tab, ai_tab = st.tabs(
        [
            "📋 企業情報",
            "✏️ 編集",
            "🤖 AI生成履歴",
        ]
    )

    # -----------------------------
    # 企業情報
    # -----------------------------

    with detail_tab:

        st.markdown("### 求人票")

        if company["job_posting"]:
            st.text_area(
                "保存済み求人票",
                value=company["job_posting"],
                height=260,
                disabled=True,
                key=f"posting_{company_id}",
            )

        else:
            st.info(
                "求人票はまだ登録されていません。"
            )

        st.markdown("### メモ")

        if company["memo"]:
            st.write(company["memo"])

        else:
            st.caption(
                "メモはありません。"
            )

    # -----------------------------
    # 編集
    # -----------------------------

    with edit_tab:

        render_company_edit_form(company)

    # -----------------------------
    # AI成果物
    # -----------------------------

    with ai_tab:

        render_company_artifacts(company_id)


def render_company_edit_form(company):
    """
    登録済み企業を編集します。
    """

    company_id = company["id"]

    with st.form(
        f"company_edit_form_{company_id}"
    ):

        company_name = st.text_input(
            "企業名",
            value=company["company_name"],
        )

        job_title = st.text_input(
            "応募職種",
            value=company["job_title"] or "",
        )

        job_url = st.text_input(
            "求人URL",
            value=company["job_url"] or "",
        )

        try:
            status_index = COMPANY_STATUSES.index(
                company["status"]
            )

        except ValueError:
            status_index = 0

        status = st.selectbox(
            "選考状況",
            COMPANY_STATUSES,
            index=status_index,
        )

        priority = st.slider(
            "志望度",
            min_value=1,
            max_value=5,
            value=company["priority"],
        )

        job_posting = st.text_area(
            "求人票",
            value=company["job_posting"] or "",
            height=220,
        )

        memo = st.text_area(
            "メモ",
            value=company["memo"] or "",
            height=140,
        )

        update_submitted = st.form_submit_button(
            "変更を保存する",
            type="primary",
        )

    if update_submitted:

        if not company_name.strip():
            st.error(
                "企業名は空欄にできません。"
            )

        else:
            try:
                update_company(
                    company_id=company_id,
                    company_name=company_name,
                    job_title=job_title,
                    job_url=job_url,
                    job_posting=job_posting,
                    status=status,
                    priority=priority,
                    memo=memo,
                )

                st.success(
                    "企業情報を更新しました。"
                )

                st.rerun()

            except Exception as e:
                st.error(
                    "企業情報を更新できませんでした。"
                    "入力内容を確認してください。"
                )

                st.code(str(e))

    st.divider()

    st.warning(
        "企業を削除すると、"
        "今後この企業に紐付けたAI生成結果も削除されます。"
    )

    confirm_delete = st.checkbox(
        "削除することを確認しました",
        key=f"delete_confirm_{company_id}",
    )

    if st.button(
        "この企業を削除する",
        key=f"delete_company_{company_id}",
    ):

        if not confirm_delete:

            st.error(
                "削除する場合は、確認チェックを入れてください。"
            )

        else:

            try:
                delete_company(company_id)

                st.success(
                    "企業を削除しました。"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    "企業を削除できませんでした。"
                )

                st.code(str(e))


def render_company_artifacts(company_id: int):
    """
    企業に紐付いているAI生成結果を表示します。

    Phase6-1時点ではまだ空の場合が多いですが、
    次のPhaseで求人分析などと接続します。
    """

    artifacts = get_company_artifacts(
        company_id
    )

    if not artifacts:

        st.info(
            """
            まだこの企業に紐付いたAI生成結果はありません。

            次のPhaseで、

            ・求人分析
            ・職務経歴書
            ・企業研究
            ・面接対策

            をここへ集約します。
            """
        )

        return

    for artifact in artifacts:

        title = (
            artifact["title"]
            or artifact["type"]
        )

        with st.expander(
            f"{title}｜{artifact['created_at']}"
        ):

            st.markdown(
                artifact["result"]
            )