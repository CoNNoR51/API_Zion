import json

import requests

if __name__ == '__main__':
    a = requests.get('http://127.0.0.1:5000/get_id/')
    convertedDict = json.loads(a.text)
    print("After conversion: ", convertedDict)

    requests.get('http://127.0.0.1:5000/net_start/', data={'id': convertedDict['id']})

    requests.post("http://127.0.0.1:5000/link_change/", data={'id': convertedDict['id'],
                                                              'loss': '0', 'delay': '2'})

    requests.get("http://127.0.0.1:5000/get_speed/", data={'id': convertedDict['id']})

    requests.post("http://127.0.0.1:5000/link_change/", data={'id': convertedDict['id'],
                                                              'loss': '12', 'delay': '33'})

    requests.get("http://127.0.0.1:5000/get_speed/", data={'id': convertedDict['id']})

    requests.post("http://127.0.0.1:5000/link_change/", data={'id': convertedDict['id'],
                                                              'loss': '100', 'delay': '90'})

    requests.get("http://127.0.0.1:5000/get_speed/", data={'id': convertedDict['id']})

    requests.get('http://127.0.0.1:5000/net_stop/')