from flask import Flask, request
from IvarCoin.BlockChain import Element
from IvarCoin.CheckWork import validate_
import requests
import os
import logging
import pickle
import socket

"""
"""
peer_list = ["http://0.0.0.0:8080/", "http://0.0.0.0:8081/", "http://0.0.0.0:8082/"]
app = Flask(__name__)
e = Element(peer_list)


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
        data = {"string": string_, "data": response}
        for peer_ip in peer_list:
            connection = peer_ip.replace("0.0.0.0", "localhost")
            peer_connection = connection + "register/chain/"
            try:
                x = requests.post(peer_connection, json=data)
                logging.debug("")
            except Exception:
                print("X_X")
                pass

        return list(response.keys())[0], 200

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


@app.route("/register/new_peer/", methods=["POST"])
def register_new_peer():
    peer_address = request.json["node_address"]
    if peer_address:
        temp_list = peer_list
        if peer_address not in peer_list:
            peer_list.append(peer_address)
            return temp_list, 200
        else:
            return "Already added", 400
    else:
        return "Node address not there", 400


@app.route("/chain_dump/", methods=["POST"])
def send_chain():
    node_address = request.json("node_address")
    if check_if_empty() is False:
        with open(get_path(), "rb") as fp:
            node_list = pickle.load(fp)
            if node_address not in node_list:
                node_list.append(node_address)
                with open(get_path(), "wb") as fp:
                    pickle.dump(node_list, fp)
            return get_all()
    else:
        return ""


@app.route("/register/chain/", methods=["POST"])
def register_new_chain_element():
    data = request.json["data"]
    string = request.json["string"]
    print(data, string)
    if not data or not string:
        return "No data/string was found with the request", 400
    else:
        e.add(data, string, state=True)
        return "Success", 200


@app.route("/test_connection/")
def test_connection():
    return "still a active peer", 200


def get_path():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "Data/peer_list.txt")
    file_path = file_path.replace("/Scripts", "/IvarCoin")
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
