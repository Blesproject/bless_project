import json, requests

def send_http(url, data = None, headers=None):
    send = requests.post(url, json=data, headers=headers)
    respons = send.json()
    return respons

def get_http(url, headers=None):
    send = requests.get(url, headers=headers)
    respons = send.json()
    return respons