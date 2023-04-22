import asyncio
import threading
from aiogram import executor
from flask import Flask, render_template, request, redirect, flash
from loginform import LoginForm

app = Flask(__name__)


@app.route('/chat')
def hello_world():  # put application's code here
    return render_template('chat.html')


@app.route('/profile')
@app.route('/index')
def index():  # put application's code here
    return render_template('base.html')


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



# def start_async_server():
#     nest_asyncio.apply()
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(run_bot())
#
#
# class MyServer(threading.Thread):
#     """ Класс потока для запуска парсинга"""
#
#     def __init__(self):
#         super().__init__()
#
#     def run(self) -> None:
#         app.run()
#
#
# if __name__ == '__main__':
#     ws = executor()
#     # thread = threading.Thread(target=start_async_server)
#     # thread.start()

# from flask import Flask, render_template
# from flask_socketio import SocketIO
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
#
#
# @socketio.on('message')
# def handle_message(data):
#     print(data)
#     print('received message:')


# if __name__ == '__main__':
#     socketio.run(app)
