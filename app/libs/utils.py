import json, requests

def send_http(url, data = None, headers=None):
    send = requests.post(url, json=data, headers=headers)
    respons = send.json()
    return respons