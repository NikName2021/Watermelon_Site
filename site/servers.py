import threading

from flask import Flask, render_template, request
from main import run_bot

app = Flask(__name__)


@app.route('/chat')
def hello_world():  # put application's code here
    return render_template('chat.html')


@app.route('/profile')
@app.route('/index')
def index():  # put application's code here
    return render_template('base.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():  # put application's code here
    if request.method == 'GET':
        return render_template('signin.html')
    elif request.method == 'POST':
        e = request.form['email']
        p = request.form['password']

        return '''<html>
                <head>
                    <meta http-equiv="Refresh" content="0; URL="/">
                </head>
                <body>
                </body>
            </html>'''


@app.route('/bot')
def bot():
    print(bot)


class Mybot(threading.Thread):
    """ Класс потока для запуска парсинга"""

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        run_bot()


class MyServer(threading.Thread):
    """ Класс потока для запуска парсинга"""

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        app.run()