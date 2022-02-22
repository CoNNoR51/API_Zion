from flask import Flask, request
from random import randint
from param import Params
from tower import start, link_change
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

app = Flask(__name__)
net_params = dict()
net = Mininet(topo=Topo, build=False)


@app.route('/get_id/', methods=['GET'])
def get_id():
    id = randint(10000000, 999999999)
    print(id)

    global net_params
    net_params.update({id: None})

    return {'id': id}


@app.route('/net_start/')
def net_start():
    id = int(request.form['id'])
    global net

    start(id, net)

    return "1"


@app.route('/set_loss_and_delay/', methods=['POST'])
def set_loss_and_delay():
    params = Params
    global net_params
    global net

    id = int(request.form['id'])
    params.loss = float(request.form['loss'])
    params.delay = request.form['delay'] + 'ms'
    buffer = {id: params}

    net_params.update(buffer)
    print(net_params)

    link_change(id, params.loss, params.delay)

    net_params[id].bw = net_params[id].loss

    print(net_params[id].bw)

    return "1"


@app.route('/get_bw/', methods=['GET'])
def get_bw():
    global net_params

    print(net_params[int(request.form['id'])].bw)

    print('____________________________________')
    print()

    return {'bw': net_params[int(request.form['id'])].bw}


@app.route('/net_stop/', methods=['GET'])
def net_stop():
    """Stopping network"""
    global net

    net.stop()

    return "1"




if __name__ == '__main__':
    app.run()
