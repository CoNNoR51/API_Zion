from flask import Flask, request
from random import randint
from param import Params

app = Flask(__name__)
net_params = dict()


@app.route('/get_id/', methods=['GET'])
def get_id():
    id = randint(1000000000000000000, 99999999999999999999)
    print(id)
    global net_params
    net_params.update({id: None})
    return {'id': id}


@app.route('/set_loss_and_delay/', methods=['POST'])
def set_loss_and_delay():
    params = Params
    id = int(request.form['id'])
    params.loss = request.form['loss']
    params.delay = request.form['delay']
    buffer = {id: params}
    global net_params
    net_params.update(buffer)
    print(net_params)

    net_params[id].bw = net_params[id].loss + net_params[id].delay

    print(net_params[id].bw)

    return "1"


@app.route('/get_bw/', methods=['GET'])
def get_bw():
    print(net_params[int(request.form['id'])].bw)
    return {'bw': net_params[int(request.form['id'])].bw}


if __name__ == '__main__':
    app.run()
