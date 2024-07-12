import nltk
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from nltk.sentiment import SentimentIntensityAnalyzer

from app import db
from app.forms import AnalyzeForm, LoginForm, RegistrationForm
from app.models import User

nltk.download("vader_lexicon")

main = Blueprint("main", __name__, static_folder="static")
auth = Blueprint("auth", __name__, static_folder="static")


@main.route("/")
@main.route("/index")
def index():
    return render_template("index.html")


@main.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    form = AnalyzeForm()
    if form.validate_on_submit():
        text = form.text.data
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(text)
        return render_template("analyze.html", form=form, sentiment=sentiment)
    return render_template("analyze.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user)
        return redirect(url_for("main.index"))
    return render_template("login.html", title="Login", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
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
