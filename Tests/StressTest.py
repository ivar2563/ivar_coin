from IvarCoin.ProofOfWork import generate
import requests
import json

"""
This code will create 10 nodes. 
The code saves proof of work strings and will try to use the string again
Which should not be possible 
In the "chain.log" there should be 10 "200" and 10 "400" responses 

"""

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
        x = requests.post("http://localhost:8081/api/add_node/", json=data)
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
        x = requests.post("http://localhost:8081/api/add_node/", json=data)
        if x.status_code == 200:
            print(x.content)


for a in range(10):
    test()

test2()
