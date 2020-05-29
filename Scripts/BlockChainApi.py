from flask import Flask, request, copy_current_request_context
from IvarCoin.BlockChain import Element
from IvarCoin.CheckWork import validate_
import requests
import concurrent.futures
from threading import Thread
import atexit
import os
import logging
import time
import pickle
import socket
import sys

"""
"""
peer_list = []
app = Flask(__name__)

e = Element(peer_list)
node_address = ""
startup_peers = []


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
        data = {"string": string_, "data": response, "node_address": request.host_url}
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
    response = {"data": e.get_last()}
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

    peer_address = request.json["data"]
    print(peer_address)
    if peer_address:
        if peer_address not in peer_list:
            response = {"data": peer_list}
            peer_list.append(peer_address)
            return response, 200
        else:
            return "Already added", 400
    else:
        return "Node address not there", 400


@app.route("/register/exiting_peer/", methods=["GET"])
def existing_peer():
    own_address = request.host_url
    data = {"node_address": own_address}
    print("peer ", own_address)
    data1 = {
        "chain": e.get_all(),
        "length": len(e.get_all())
    }
    if not own_address:
        return "something went wrong", 400
    else:
        for peer in peer_list:
            try:
                if "0.0.0.0" in peer:
                    peer = peer.replace("0.0.0.0", "localhost")

                print(peer + "register/new_peer/")
                response = requests.post(peer + "register/new_peer/", json=data)
                if response.status_code == 200:
                    if type(response.content) == list:
                        for p in response.content:
                            if p not in peer_list:
                                peer_list.append(p)
            except ConnectionError as _:
                print(_)
                pass

        return data1, 200


@app.route("/test/", methods=["GET"])
def test():
    x = requests.get(request.host_url + "register/exiting_peer/")
    print(x)
    return x.content, 200


@app.route("/chain_dump/", methods=["POST"])
def send_chain():
    node_address = request.remote_addr
    print(node_address)
    if node_address:
        peer_list.append(node_address)
        return e.get_all()
    else:
        return "No valid address given"


@app.route("/register/chain/", methods=["POST"])
def register_new_chain_element():
    data = request.json["data"]
    string = request.json["string"]
    address = request.json["node_address"]
    if address not in peer_list:
        peer_list.append(address)
    if not data or not string:
        return "No data/string was found with the request", 400
    else:
        address = request.remote_addr
        temp_list = peer_list
        if address in temp_list:
            temp_list.remove()
        if address not in temp_list:
            peer_list.append(address)
        logging.debug(address)
        temp_list.remove(address)
        e.add(data, string, state=True)
        return "Success", 200


@app.route("/test_connection/", methods=["GET"])
def test_connection():
    return "still a active peer", 200


@app.route("/test2/", methods=["GET"])
def test2():
    x = request.host_url
    return x


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 0))
port = sock.getsockname()[1]
sock.close()
host = '0.0.0.0'


def start_up(startup_peers):
    data = {"data": "http://{}:{}/".format(host, port)}
    for peer in startup_peers:
        print(peer)
        try:
            logging.debug("start")
            if "0.0.0.0" in peer:
                peer = peer.replace("0.0.0.0", "localhost")
            x = peer + "register/new_peer/"
            print("sssssssssssssssssssssssssssssss")
            print(x)
            print(data)
            logging.debug("over requests")
            r = requests.post(x, json=data)
            print("----", r)
            logging.debug("after requests")
            response = dict(r.json())
            logging.debug("after jsoinifying")
            logging.debug("mid")
            if int(r.status_code) == 200 and isinstance(response, dict):
                logging.debug(peer)
                print(response)
                if peer not in peer_list:
                    peer_list.append(peer)
                print("TRUE")
                logging.debug("end")
                for a in response["data"]:
                    if a not in startup_peers:
                        peer_list.append(a)
            else:
                logging.debug("One of the startup nodes did not respond or it did not work")
        except OSError:
            logging.critical("Startup failed, node is useless")
            print("Unexpected error:", sys.exc_info())
            pass


class FlaskThread(Thread):
    def run(self):
        app.run(host=host, port=port)


def main():
    start_addresses = sys.argv
    start_addresses.remove(start_addresses[0])
    if len(start_addresses) >= 1:
        if len(start_addresses) > 1:
            for address in start_addresses:
                startup_peers.append(address)
        else:
            startup_peers.append(start_addresses[0])
    server = FlaskThread()
    server.daemon = True
    server.start()
    time.sleep(2)
    start_up(startup_peers)
    server.join()


if __name__ == "__main__":
    main()
