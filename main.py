from flask import Flask, request
from random import randint
from mininet.link import TCLink
from param import Params
from mn_functions import start
from mininet.net import Mininet
from mininet.log import setLogLevel
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
net_params = dict()
net = Mininet(link=TCLink, build=False)


@app.route('/get_id/', methods=['GET'])
def get_id():
    id = randint(10000000, 999999999)
    print(id)

    global net_params
    net_params.update({id: None})

    return {'id': id}


@app.route('/net_start/', methods=['GET'])
def net_start():
    global net
    id = int(request.form['id'])

    start(id, net)

    return "1"


@app.route('/link_change/', methods=['POST'])
def link_change():
    params = Params
    global net_params
    global net

    id = int(request.form['id'])
    params.loss = float(request.form['loss'])
    params.delay = request.form['delay'] + 'ms'
    buffer = {id: params}

    net_params.update(buffer)
    print(net_params)

    net.delLinkBetween(net.get('h' + str(id)), net.get('s1'), allLinks=True)
    net.addLink(net.get('h' + str(id)), net.get('s1'),
                loss=net_params[id].loss, delay=net_params[id].delay)
    net.build()

    return "1"


@app.route('/get_speed/', methods=['GET'])
def get_speed():
    global net_params
    global net
    buf = ''
    write = False
    id = int(request.form['id'])

    host = net.get('h' + str(id))

    result = host.cmd('ping -c 1 -q 10.0.0.1')
    print(result)

    for char in result:
        if char == '/':
            write = False

        if write:
            buf += char

        if char == '=':
            write = True

    print(buf)

    if buf == '':
        net_params[id].speed = 0
    else:
        time_for_pkg = float(buf)
        print(buf)
        net_params[id].speed = 0.4375 / (time_for_pkg / 1000)

    return {'speed': net_params[id].speed}


@app.route('/net_stop/', methods=['GET'])
def net_stop():
    """Stopping network"""
    global net

    net.stop()
    print('net stopped')

    return "1"


if __name__ == '__main__':
    setLogLevel('info')
    app.run()
