from flask import Flask, request
from random import randint
from mininet.link import TCLink
from param import Params
from mn_functions import start, link_change_mn, get_speed_mn
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
    par = Params()
    par.loss = 0
    par.delay = '5ms'
    id = randint(10000000, 999999999)

    global net_params
    net_params.update({id: par})

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

    link_change_mn(net, id, net_params[id].loss, net_params[id].delay)

    return "1"


@app.route('/get_speed/', methods=['GET'])
def get_speed():
    global net_params
    global net

    id = int(request.form['id'])

    net_params[id].speed = get_speed_mn(net, id)

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
