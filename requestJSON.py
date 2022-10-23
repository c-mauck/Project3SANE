import requests
import time
import json

# This works, it's necessary that the URL's match
ip = "127.0.0.1"


# Code to post a change
def post2count(num):
    global ip
    req = requests.post(f'http://{ip}:5000/api/counter', json={"add": num})
    if req.ok:
        print(req.json())
    else:
        print("Error: " + str(req.status_code))


# Code to get the count
def getcount():
    global ip
    req = requests.get(f'http://{ip}:5000/api/counter')
    print(f'http://{ip}:5000/api/counter')
    if req.ok:
        print(req.json())
    else:
        print("Error: " + str(req.status_code))

# BROKEN do not use
def getpage():
    """Broken, do not use"""
    global ip
    req = requests.get(f'http://{ip}:5000')
    if req.ok:
        print(req.json())
    else:
        print("Error: " + str(req.status_code))


if __name__ == "__main__":
    time.sleep(10)
    post2count(1)
    time.sleep(1)
    post2count(3)
    time.sleep(3)
    post2count(-2)
    time.sleep(3)
    getcount()

