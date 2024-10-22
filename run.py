from app import create_app, db
from app.models import User  # モデルのインポートを追加

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # データベースとテーブルを作成
    app.run(debug=True)