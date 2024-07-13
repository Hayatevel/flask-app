import nltk
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from nltk.sentiment import SentimentIntensityAnalyzer

from app import db
from app.forms import AnalyzeForm, LoginForm, RegistrationForm
from app.models import User

nltk.download("vader_lexicon")  # 自然言語ライブラリをダウンロード

# Blueprintの設定
main = Blueprint("main", __name__, static_folder="static")
auth = Blueprint("auth", __name__, static_folder="static")


@main.route("/")
@main.route("/index")
def index():
    """インデックスページへのルーティング

    Returns:
        render_template: str
    """
    return render_template("index.html")


@main.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    """解析ページへのルーティング

    Returns:
        render_template: str
    """
    form = AnalyzeForm()
    if form.validate_on_submit():
        text = form.text.data  # ユーザーがテキストフォームに入力した文字列データ
        sia = SentimentIntensityAnalyzer()  # 自然言語ライブラリをインスタンス化
        sentiment = sia.polarity_scores(text)  # 文字列データを解析
        return render_template("analyze.html", form=form, sentiment=sentiment)
    return render_template("analyze.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """ログインページへのルーティング

    Returns:
        render_template: str
    """
    if current_user.is_authenticated:
        # すでにログイン済みユーザーからのリクエストならインデックスページにリダイレクト
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # ユーザー名とパスワードの確認
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user)  # ユーザーセッションイン
        return redirect(url_for("main.index"))
    return render_template("login.html", title="Login", form=form)


@auth.route("/logout")
def logout():
    """ログアウトページへのルーティング

    Returns:
        render_template: str
    """
    logout_user()  # ユーザーのセッションアウト
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    """サインアップページ(アカウント作成)ページへのルーティング

    Returns:
        render_template: str
    """
    if current_user.is_authenticated:
        # すでにログイン済みユーザーからのリクエストならインデックスページにリダイレクト
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("auth.login"))
    return render_template("register.html", title="Register", form=form)
