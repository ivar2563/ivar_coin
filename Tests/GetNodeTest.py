import requests

"""
If you want to get a node back
u can give tha variable called string your receipt
"""


def get_node_test():
    string = {"receipt": "a0aebace-ef47-4cfc-9605-19d02a6d0864"}
    response = requests.post("http://localhost:8080/api/get_node/", json=string)
    print(response.content)


get_node_test()