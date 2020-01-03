from BlockChain.ProofOfWork import generate
import requests
import json

email = "Ola.norman@lyse.net"
bits = 20

list_ = []


def test():
    while True:
        x = generate(email, bits)
        list_.append(x)
        data = {
            "data": [2, "pro", {"x23": "2s"}, ["sda", 242]],
            "string": x
        }
        x = requests.post("http://127.0.0.1:5000/api/add_node/", json=data)
        if x.status_code == 200:
            print(x.content)
            break

    print(x)


def test2():
    for a in list_:
        data = {
            "data": [2, "pro", {"x23": "2s"}, ["sda", 242]],
            "string": a
        }
        x = requests.post("http://127.0.0.1:5000/api/add_node/", json=data)
        if x.status_code == 200:
            print(x.content)


for a in range(10):
    test()

test2()
