import secrets

from flask import Flask, request, render_template, redirect, url_for, session

from connectors.articles import ArticlesConnector
from connectors.authentication import AuthConnector

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
auth_connector = AuthConnector()
articles_connector = ArticlesConnector()


@app.route('/', methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        try:

            username = request.form.get("loginUsername")
            password = request.form.get("loginPassword")
            assert username, 'O nome de usuário deve estar preenchido'
            assert password, 'A senha deve estar preenchida'

            user_data = auth_connector.user_login({"username": username, "password": password})
            jwt_token = user_data.get('access_token')

            session['jwt_token'] = jwt_token
            return redirect(url_for('home'))

        except Exception as err:
            error = err

    return render_template("login.html", error=error)


@app.route('/home', methods=["GET", "POST", "PUT"])
def home():
    articles = None
    error = None
    try:
        if not session.get('jwt_token') or request.method == 'PUT':
            return redirect(url_for('login'))

        if request.method == 'POST':
            articles = articles_connector.get_articles()

    except Exception as err:
        error = err

    return render_template("home.html", articles=articles, error=error)


@app.route('/logout', methods=["POST"])
def logout():
    session['jwt_token'] = None
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)
