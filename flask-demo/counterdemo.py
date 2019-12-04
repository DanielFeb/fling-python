import json

from flask import Flask, session
from flask import render_template
from flask import request
from flask_socketio import SocketIO

from counter import Counter

port = 5000
app = Flask(__name__)
socket_io = SocketIO(app)


@socket_io.on('connect')
def test_connect():
    session["sid"] = request.sid
    print(request.sid + " connect!")
    socket_io.emit('my response', {'data': 'Connected'}, room=request.sid)
    """客户端连接"""
    sid = request.sid  # io客户端的sid, socketio用此唯一标识客户端.
    can = False
    host = request.host.split(":")[0]
    host_list = ['127.0.0.1', "0.0.0.0"]
    """
    根据页面的访问地址决定是否允许连接, 你可以自己实现自己对访问的控制逻辑.
    最后决定是允许连接还是使用socket_io.server.disconnect(sid)断开链接.
    """
    if host in host_list:
        can = True
    elif host.startswith("192.168") or host.startswith("local"):
        can = True
    else:
        pass
    if not can:
        socket_io.emit(event="connecting", data=json.dumps({"message": "connect refuse!"}))
        socket_io.server.disconnect(sid)


@socket_io.on('disconnect')
def test_connect():
    stop()
    print(request.sid + " disconnect!")


@socket_io.on("start")
def start_func(data):
    counter = Counter(data['data'] if data['data'] else 0)
    session["counter"] = counter
    run()


def run():
    counter = session["counter"]
    counter.run()
    while counter.isRunning:
        print(request.sid + " running")
        socket_io.emit(event="mes", data=counter.process(), room=request.sid)
    print(request.sid + " stop")
    socket_io.emit(event="mes", data="stopped", room=request.sid)


def stop():
    counter = session["counter"]
    counter.stop()


@socket_io.on("stop")
def stop_func(data):
    stop()


@socket_io.on("continue")
def stop_func(data):
    run()


@app.route("/counter")
def test_func():
    """测试页面"""
    return render_template("counter.html")


if __name__ == '__main__':
    socket_io.run(app=app, host="0.0.0.0", port=port, debug=True)
