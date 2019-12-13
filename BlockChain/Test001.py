from BlockChain.ProofOfWork import generate
import requests
import json

email = "Ola.norman@lyse.net"
bits = 20

data = {
    "data": [2, "pro", {"x23": "2s"}, ["sda", 242]],
    "string": generate(email, bits)
}


print(data)
print(requests.post("http://127.0.0.1:5000/api/add_node/", json=data))

