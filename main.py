from flask import Flask, request
from random import randint
from param import Params
from tower import simple_test

app = Flask(__name__)
net_params = dict()


@app.route('/get_id/', methods=['GET'])
def get_id():
    id = randint(10000000, 999999999)
    print(id)

    global net_params
    net_params.update({id: None})

    return {'id': id}


@app.route('/set_loss_and_delay/', methods=['POST'])
def set_loss_and_delay():
    params = Params
    global net_params

    id = int(request.form['id'])
    params.loss = float(request.form['loss'])
    params.delay = request.form['delay'] + 'ms'
    buffer = {id: params}

    net_params.update(buffer)
    print(net_params)

    simple_test(id, params.loss, params.delay)

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


if __name__ == '__main__':
    app.run()
