from BlockChain.ProofOfWork import generate
import requests
import json

email = "Ola.norman@lyse.net"
bits = 20




def test():
    while True:
        data = {
            "data": [2, "pro", {"x23": "2s"}, ["sda", 242]],
            "string": generate(email, bits)
        }
        x = requests.post("http://127.0.0.1:5000/api/add_node/", json=data)
        if x.status_code == 200:
            print(x.content)
            break

    print(x)


for a in range(100):
    test()
