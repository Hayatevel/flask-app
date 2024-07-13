from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """データベースを作成

    Args:
        UserMixin (object): 外部ライブラリ
        db (data): データベース
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        """パスワードをハッシュ化

        Args:
            password (str): ユーザーが入力したパスワード
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """フォームに入力されたパスワードをチェック

        Args:
            password (str): ユーザーが入力したパスワード

        Returns:
            check_password_hash: ハッシュ化された文字列
        """
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
