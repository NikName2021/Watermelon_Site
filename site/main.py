import sqlite3

from flask import Flask, url_for, request, redirect, render_template, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash

import loginform

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key_03453423023'


@app.route('/')
def top():
    try:
        if session['logined']:
            log = session['login']
            if session['is_admin']:
                rol = "Администратор"
            else:
                rol = "Пользователь"
            return render_template('main.html', title='Главное меню', login=log, is_admin=rol)
        else:
            return redirect('/login')
    except:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginform.LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM users
                    WHERE login = '{name}' AND password = '{password}'""").fetchall()
        if result:
            session['logined'] = True
            session['login'] = str(result[0][0])
            if result[0][2] == "True":
                session['is_admin'] = True
            else:
                session['is_admin'] = False
        con.close()
        return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    session['logined'] = False
    return redirect('/')


@app.route('/phrases')
def phrases():
    try:
        if session['logined']:
            con = sqlite3.connect("users.db")
            cur = con.cursor()
            result = cur.execute("""SELECT * FROM phrases""").fetchall()
            log = session['login']
            if session['is_admin']:
                rol = "Администратор"
            else:
                rol = "Пользователь"
            con.close()
            return render_template('phrase.html', title="Фразы дня", phrases=result, login=log, is_admin=rol)
        else:
            return redirect('/login')
    except:
        return redirect('/login')


@app.route('/addp', methods=['GET', 'POST'])
def addp():
    form = loginform.AddPhrase()
    log = session['login']
    if session['is_admin']:
        rol = "Администратор"
    else:
        rol = "Пользователь"
    if form.validate_on_submit():
        u = form.phrase.data
        print(u)
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM phrases""").fetchall()
        cur.execute(f"""INSERT INTO phrases VALUES({result[-1][0] + 1}, "{u}")""").fetchall()
        con.commit()
        con.close()
        return redirect('/phrases')
    return render_template('phraseadd.html', title='Добавить фразу', form=form, login=log, is_admin=rol)


@app.route('/delp', methods=['GET', 'POST'])
def delp():
    form = loginform.DelPhrase()
    log = session['login']
    if session['is_admin']:
        rol = "Администратор"
    else:
        rol = "Пользователь"
    if form.validate_on_submit():
        u = int(form.phrase.data) - 1
        print(u)
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute(f"""DELETE from phrases where id = {u}""").fetchall()
        con.commit()
        con.close()
        return redirect('/phrases')
    return render_template('phrasedel.html', title='Удалить фразу', form=form, login=log, is_admin=rol)


@app.route('/add')
def add():
    try:
        if session['logined'] and session['is_admin']:
            con = sqlite3.connect("users.db")
            cur = con.cursor()
            result = cur.execute("""SELECT * FROM users""").fetchall()
            log = session['login']
            if session['is_admin']:
                rol = "Администратор"
            else:
                rol = "Пользователь"
            con.close()
            return render_template('users.html', title="Пользователи", phrases=result, login=log, is_admin=rol)
        else:
            return redirect('/login')
    except:
        return redirect('/login')


@app.route('/addu', methods=['GET', 'POST'])
def addu():
    form = loginform.AddUser()
    log = session['login']
    if session['is_admin']:
        rol = "Администратор"
    else:
        rol = "Пользователь"
    if form.validate_on_submit():
        u = form.login.data
        p = form.password.data
        a = form.is_admin.data
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute(f"""INSERT INTO users VALUES('{u}', '{p}', '{a}')""").fetchall()
        con.commit()
        con.close()
        return redirect('/add')
    return render_template('useradd.html', title='Добавить пользователя', form=form, login=log, is_admin=rol)


@app.route('/delu', methods=['GET', 'POST'])
def delu():
    form = loginform.DelUser()
    log = session['login']
    if session['is_admin']:
        rol = "Администратор"
    else:
        rol = "Пользователь"
    if form.validate_on_submit():
        u = form.phrase.data
        print(u)
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute(f"""DELETE from users where login = '{u}'""").fetchall()
        con.commit()
        con.close()
        return redirect('/add')
    return render_template('userdel.html', title='Удалить пользователя', form=form, login=log, is_admin=rol)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')