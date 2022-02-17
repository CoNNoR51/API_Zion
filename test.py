import json

import requests

if __name__ == '__main__':
    a = requests.get('http://127.0.0.1:5000/get_id/')
    convertedDict = json.loads(a.text)
    print("After conversion: ", convertedDict)

    requests.post("http://127.0.0.1:5000/set_loss_and_delay/", data={'id': convertedDict['id'],
                                                                     'loss': '12', 'delay': '33'})
    # requests.post("http://127.0.0.1:5000/set_loss_and_delay/", data={'id': '45826874156537428596',
    #                                                                  'loss': '77', 'delay': '89'})
    w = requests.get('http://127.0.0.1:5000/get_bw/', data={'id': convertedDict['id']})

    convertedDict1 = json.loads(w.text)
    print("After conversion: ", convertedDict1)