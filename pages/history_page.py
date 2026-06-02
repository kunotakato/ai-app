import streamlit as st

from services.history_manager import (
    get_generation_history,
    get_generation_history_by_id,
    delete_generation_history,
)


def render_history_page():
    """
    生成履歴ページです。
    """

    st.title("📚 生成履歴")
    st.caption("これまでに生成した結果を一覧で確認できます。")

    histories = get_generation_history()

    if not histories:
        st.info("まだ生成履歴はありません。")
        return

    history_options = {
        f"{item['id']}｜{item['created_at']}｜{item['type']}｜{item['input_summary']}": item["id"]
        for item in histories
    }

    selected_label = st.selectbox(
        "表示する履歴を選択してください",
        list(history_options.keys()),
    )

    selected_id = history_options[selected_label]
    selected_history = get_generation_history_by_id(selected_id)

    if not selected_history:
        st.error("履歴が見つかりませんでした。")
        return

    st.subheader("履歴詳細")

    st.write(f"作成日時：{selected_history['created_at']}")
    st.write(f"種別：{selected_history['type']}")
    st.write(f"現在の職種：{selected_history['current_job']}")
    st.write(f"希望職種：{selected_history['target_job']}")
    st.write(f"入力概要：{selected_history['input_summary']}")

    st.markdown(selected_history["result"])

    st.text_area(
        "コピー用",
        value=selected_history["result"],
        height=420,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Markdownでダウンロード",
            data=selected_history["result"],
            file_name=f"history_{selected_history['id']}.md",
            mime="text/markdown",
        )

    with col2:
        if st.button("この履歴を削除"):
            delete_generation_history(selected_history["id"])
            st.success("履歴を削除しました。")
            st.rerun()