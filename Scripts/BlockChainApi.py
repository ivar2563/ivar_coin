from flask import Flask, request
from IvarCoin.BlockChain import Element
from IvarCoin.CheckWork import validate_
import os
import logging
import pickle

"""
"""

app = Flask(__name__)
e = Element()


@app.route("/api/add_node/", methods=["POST"])
def add_node():
    """
    Will add a node
    it needs proof of work string
    for now it needs some sort of data
    :return:
    """
    string_ = request.json["string"]
    data = request.json["data"]
    string_response = validate_(string_)
    if string_response is True:
        response = e.add_element(data, string_)
        data = {"string": string_, "data": data}
        if check_if_empty() is True:
            with open(get_path(), "rb") as fp:
                node_ips = pickle.load(fp)
        for node_ip in node_ips:
            _ = request.post(node_ip[0] + "/register/chain", data)
        return response, 200
    else:
        return "The string was already used, or its wrong", 400


@app.route("/api/get/all/", methods=["GET"])
def get_all():
    """
    Will get all of the nodes
    :return:
    """
    x = e.get_all()
    response = {"data": x}
    return response


@app.route("/api/get/first/", methods=["GET"])
def get_first():
    """
    Will get the first element in the chain
    :return:
    """
    x = e.get_first()
    response = {"data": x}
    return response


@app.route("/api/get/last/", methods=["GET"])
def get_last():
    """
    Will get the last element in the chain
    :return:
    """
    x = e.get_last()
    response = {"data": x}
    return response


@app.route("/api/get_node/", methods=["POST"])
def get_node_with_receipt():
    """
    Will get the node associated with the receipt
    :return:
    """
    receipt = request.json["receipt"]
    node = e.get_node(receipt)
    return node


@app.route("/register/new_node/", methods=["POST"])
def register_new_peer():
    peer_address = request.json["node_address"]
    if peer_address:
        if check_if_empty() is True:
            node_list = []
        if check_if_empty() is False:
            with open(get_path(), "rb") as fp:
                node_list = pickle.load(fp)
        if peer_address not in node_list:
            with open(get_path(), "wb") as fp:
                node_list.append(peer_address)
                pickle.dump(node_list, fp)
            return e.get_all(), 200
        else:
            return "Already added", 400
    else:
        return "Node address not there", 400

@app.route("/chain_dump/")
def send_chain():
    node_address = request.json("node_address")
    check_if_empty()
    with open(get_path(), "rb") as fp:
        node_list = pickle.load(fp)
        if node_address not in node_list:
            node_list.append(node_address)
            with open(get_path(), "wb") as fp:
                pickle.dump(node_list, fp)
        return get_all()
    return ""


@app.route("/register/chain")
def register_new_chain_element():
    data = request.json["data"]
    string = request.json["string"]
    if not data or not string:
        return 400, "No data/string was found with the request"
    else:
        e.add(data, string, state=True)


@app.route("/test_connection/")
def test_connection():
    return "still a active peer", 200


def get_path():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "Data/node_id.txt")
    return file_path


def check_if_empty():
    """
    Will check if the pickle list is empty
    :return:
    """
    try:
        with open(get_path(), 'rb') as fp:
            _ = pickle.load(fp)
        return False
    except EOFError:
        return True
    except FileNotFoundError:
        with open(get_path(), "wb") as fp:
            empty_list = []
            pickle.dump(empty_list, fp)
            return True


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    x = Element()
    x.validate_chain()
