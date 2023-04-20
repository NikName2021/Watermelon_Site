from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/chat')
def hello_world():  # put application's code here
    return render_template('chat.html')


@app.route('/')
@app.route('/index')
def index():  # put application's code here
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run()


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


if __name__ == '__main__':
    socketio.run(app)
