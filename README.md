# CareerCraft AI

CareerCraft AIは、転職希望者向けのAI転職支援ツールです。

職務経歴書の作成だけでなく、キャリア整理、自己分析、求人分析、面接対策、生成履歴管理まで行えます。

## 作成目的

転職活動では、以下のような悩みが起きやすいです。

- 自分の強みが分からない
- 職務経歴書に何を書けばいいか分からない
- 求人票を見ても自分に合うか判断できない
- 面接で何を聞かれるか不安
- 過去に作った文章を見返せない

CareerCraft AIは、これらの作業をAIで支援し、転職活動の準備時間を短縮することを目的に作成しました。

## 主な機能

- キャリア地図作成
- 自己分析・職種診断
- 求人票分析
- 求人票スクショ読み取り
- マッチ率表示
- 職務経歴書生成
- Markdown / Word / PDF出力
- 面接対策生成
- SQLiteによる生成履歴保存
- 生成履歴の再表示・削除

## 使用技術

- Python
- Streamlit
- OpenAI API
- SQLite
- python-docx
- reportlab
- Git / GitHub

## ファイル構成

```text
career-craft-ai/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── prompts/
├── services/
├── pages/
├── outputs/
├── data/
└── database/