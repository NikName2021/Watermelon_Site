
import sqlite3
from flask import Flask, render_template, request, redirect, flash
from loginform import LoginForm, AddPhrase
from datetime import date

app = Flask(__name__)


@app.route('/chat')
def hello_world():  # put application's code here
    return render_template('chat.html')


@app.route('/profile')
@app.route('/index')
def index():  # put application's code here
    return render_template('base.html')


@app.route('/phrases')
def phrases():
    con = sqlite3.connect("../bot/base.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM phrase""").fetchall()
    con.close()
    return render_template('phrase.html', phrases=result)


@app.route('/addp', methods=['GET', 'POST'])
def addp():
    form = AddPhrase()
    if form.validate_on_submit():
        u = form.phrase.data
        print(u)
        con = sqlite3.connect("../bot/base.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM phrase""").fetchall()
        print(result)
        cur.execute(f"""INSERT INTO phrase VALUES({result[-1][0] + 1}, "{u}", "{date.today()}")""").fetchall()
        con.commit()
        con.close()
        return redirect('/phrases')
    return render_template('phraseadd.html', title='Добавить фразу', form=form)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = form.username.data
        p = form.password.data
        return redirect('/profile')
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(port=5000)

