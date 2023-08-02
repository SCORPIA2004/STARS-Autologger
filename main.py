import requests
import json

def login(mail, password):
    s = requests.Session()
    payload = {
        '_user' : mail,
        '_pass' : password
    }
    res = s.post('https://webmail.bilkent.edu.tr/?_task=login')