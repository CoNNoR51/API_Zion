from flask import Flask, request
from random import randint
from param import Params
from tower import start, link_change
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel

app = Flask(__name__)
net_params = dict()
net = Mininet()


@app.route('/get_id/', methods=['GET'])
def get_id():
    id = randint(10000000, 999999999)
    print(id)

    global net_params
    net_params.update({id: None})

    return {'id': id}


@app.route('/net_start/', methods=['GET'])
def net_start():
    id = int(request.form['id'])
    global net

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

    # link_change(id, params.loss, params.delay)

    net.delLinkBetween(net.get('h'+str(id)), net.get('s1'), allLinks=True)
    net.addLink(net.get('h'+str(id)), net.get('s1'),
                loss=net_params[id].loss, delay=net_params[id].delay)

    return "1"


@app.route('/get_speed/', methods=['GET'])
def get_speed():
    global net_params
    global net

    print(net_params[int(request.form['id'])].speed)

    print('____________________________________')
    print()

    return {'bw': net_params[int(request.form['id'])].speed}


@app.route('/net_stop/', methods=['GET'])
def net_stop():
    """Stopping network"""
    global net

    net.stop()

    return "1"


if __name__ == '__main__':
    app.run()
