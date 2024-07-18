# flask-app
このREDME.mdをVSCODEに *"Markdown All in One"* 拡張機能をいれて `Ctrl + Shfit + v` でプレビュー表示すると見やすいです。
## テキストの感情分析アプリ
### アプリ機能
入力されたテキストに対して、ポジティブなクエリか、ネガティブなクエリかを、AIが判別して出力する
シングルページアプリケーションです！
> ~~Javaシステム開発のリーダーだったのでFlaskに割けるリソースが低く目新しい機能があまりないです~~
### アカウント機能
ユーザーのアカウント作成、ログイン、ログアウトの機能もあり、ログイン済みユーザーしかアプリを使用できないようになっています
## リソーススタック
### バックエンド
- Python 3.12.3
- Flask 2.3.3
- SQLite3
### フロントエンド(template engine)
- Jinja2
### UI
- Tailwind CSS を使いモダンでレスポンシブなデザインに
## ちょいおもろい工夫
- 適当なurlを入力してもエラーハンドリングにてカスタムされた404notFoundページに遷移します
- データベースにエラーが発生するとカスタムされた500ページへ
- MVTパターンやPRGパターンを採用し、開発保守がしやすいです
## ローカル環境構築
このREADMEがあるディレクトリに移動
```shell
python -V # pythonがインストールされていることを確認(なるべく最新バージョン推奨 < 3.11.x)

python -m venv .venv # 仮想環境作成

# 仮想環境の起動
source ./.venv/bin/activate # Linux/mac
./.venv/scripts/activate.ps1 # windows

pip install -r requirements.txt # 必要モジュールのインストール

python run.py # アプリ起動 http://127.0.0.1:5000 へアクセス
```
### 遊び方
1. アカウント作成をしログインしたらボタンを押して分析ページへ
2. 入力欄にテキストを入力して下のボタンを押すと解析結果が表示(英語のみ対応)
入力例: "Happy", "Fun", "Angry", "Sad", "Run", "Poor", "Flash"